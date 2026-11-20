# services/llm_gateway/infrastructure/anthropic_adapter.py
from anthropic import AsyncAnthropic
from app.service.analysis_service.schemas.analysis_schema import (GenerateRequest,GenerateResponse,TokenUsage)


class AnthropicAdapter:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=api_key)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        model = request.model or "claude-sonnet-4-6"

        system_prompt = next(
            (m.content for m in request.messages if m.role == "system"),
            None,
        )
        chat_messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
            if m.role != "system"
        ]

        response = await self.client.messages.create(
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=system_prompt,
            messages=chat_messages,
        )

        text = "".join(
            block.text for block in response.content if block.type == "text"
        )

        return GenerateResponse(
            text=text,
            provider="anthropic",
            model=model,
            usage=TokenUsage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            ),
        )

# app/ai/context_builder.py
"""
Builds the factual context the LLM is grounded on.

Everything here is deterministic (PostGIS + SQL). The LLM never computes or
guesses these values; it only explains them.

ASSUMPTIONS to verify against your schema (marked TODO below):
  - parcels(id, geom, address)           -> address column name
  - zoning(zone_code, ordinance_number, geom)
  - zoning_land_use_codes(code, description)
  - zoning_map_amendments(ordinance_number, adopted_date, from_zone, to_zone, has_proffer)
  - overlay layer tables and their name columns (see LAYER_TABLES)
  - all geometries share one SRID
"""
import json
from collections import Counter

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import Flag, OverlayMatch, ParcelFacts, RezoningInfo

# Ignore sliver overlaps from boundary noise (percent of the parcel's area)
MIN_OVERLAP_PCT = 1.0

# EPSG:2283 = NAD83 / Virginia North (ftUS). ST_Area on it returns square feet.
AREA_SRID = 2283

# layer key -> (table, name column). Hard-coded whitelist: these values are
# interpolated into SQL, so they must never come from user input.
LAYER_TABLES: dict[str, tuple[str, str]] = {
    "height": ("height_districts", "district"),  # TODO confirm column name
    "historic": ("historic_districts", "name"),  # TODO confirm column name
    "parking": ("parking_districts", "name"),  # TODO confirm column name
    "paid_parking": ("paid_parking_zones", "name"),  # TODO confirm column name
}

PARCEL_SQL = text(
    f"""
    SELECT p.id AS parcel_id,
           p.address AS address,  -- TODO confirm column name
           ST_Area(ST_Transform(p.geom, {AREA_SRID})) AS lot_area_sqft
    FROM parcels p
    WHERE p.id = :parcel_id
    """
)

# Zone is resolved from the parcel's representative point, which guarantees
# exactly one polygon and avoids the straddling ambiguity for the base zone.
ZONE_SQL = text(
    """
    SELECT z.zone_code,
           c.description AS zone_description,
           z.ordinance_number,
           a.adopted_date,
           a.from_zone,
           a.to_zone,
           COALESCE(a.has_proffer, false) AS has_proffer
    FROM parcels p
    JOIN zoning z
      ON ST_Intersects(z.geom, ST_PointOnSurface(p.geom))
    LEFT JOIN zoning_land_use_codes c ON c.code = z.zone_code
    LEFT JOIN zoning_map_amendments a ON a.ordinance_number = z.ordinance_number
    WHERE p.id = :parcel_id
    LIMIT 1
    """
)


def _overlay_sql(table: str, name_col: str):
    # NOTE: assumes layer geometries are valid (run ST_MakeValid at load time),
    # otherwise ST_Intersection can raise a topology exception.
    return text(
        f"""
        SELECT l.{name_col} AS name,
               100.0 * ST_Area(ST_Intersection(l.geom, p.geom))
                     / NULLIF(ST_Area(p.geom), 0) AS overlap_pct
        FROM parcels p
        JOIN {table} l ON ST_Intersects(l.geom, p.geom)
        WHERE p.id = :parcel_id
        ORDER BY overlap_pct DESC
        """
    )


async def build_parcel_facts(
    session: AsyncSession, parcel_id: int
) -> ParcelFacts | None:
    """Return computed facts for a parcel, or None if the parcel doesn't exist."""
    parcel = (
        (await session.execute(PARCEL_SQL, {"parcel_id": parcel_id}))
        .mappings()
        .first()
    )
    if parcel is None:
        return None

    zone = (
        (await session.execute(ZONE_SQL, {"parcel_id": parcel_id})).mappings().first()
    )

    overlays: list[OverlayMatch] = []
    for layer, (table, name_col) in LAYER_TABLES.items():
        rows = (
            (
                await session.execute(
                    _overlay_sql(table, name_col), {"parcel_id": parcel_id}
                )
            )
            .mappings()
            .all()
        )
        for r in rows:
            pct = float(r["overlap_pct"] or 0)
            if pct < MIN_OVERLAP_PCT:
                continue
            overlays.append(
                OverlayMatch(layer=layer, name=r["name"], overlap_pct=round(min(pct, 100.0), 1))
            )

    rezoning = None
    if zone and zone["ordinance_number"] is not None:
        rezoning = RezoningInfo(
            ordinance_number=zone["ordinance_number"],
            adopted_date=zone["adopted_date"],
            from_zone=zone["from_zone"],
            to_zone=zone["to_zone"],
            has_proffer=zone["has_proffer"],
        )

    return ParcelFacts(
        parcel_id=parcel["parcel_id"],
        address=parcel["address"],
        zone_code=zone["zone_code"] if zone else None,
        zone_description=zone["zone_description"] if zone else None,
        lot_area_sqft=round(float(parcel["lot_area_sqft"]), 1)
        if parcel["lot_area_sqft"] is not None
        else None,
        overlays=overlays,
        rezoning=rezoning,
    )


def build_flags(facts: ParcelFacts) -> list[Flag]:
    """
    Deterministic warnings. These are shown to the user even if the LLM call
    fails or the model forgets to mention them. NO_ORDINANCE_TEXT is added by
    the service when retrieval returns nothing, not here.
    """
    flags: list[Flag] = []

    if facts.rezoning and facts.rezoning.has_proffer:
        flags.append(
            Flag(
                code="PROFFER",
                severity="warning",
                message=(
                    "This parcel was rezoned with proffers. Additional binding conditions "
                    "may apply that are not part of the base zone rules."
                ),
            )
        )

    if facts.zone_code and facts.zone_code.upper().startswith("CDD"):
        flags.append(
            Flag(
                code="CDD",
                severity="warning",
                message=(
                    "This parcel is in a Coordinated Development District. Site-specific "
                    "approvals may override or add to the standard zone rules."
                ),
            )
        )

    if any(o.layer == "historic" for o in facts.overlays):
        flags.append(
            Flag(
                code="HISTORIC_DISTRICT",
                severity="warning",
                message=(
                    "This parcel is in a historic district. Exterior changes may require "
                    "design review before permitting."
                ),
            )
        )

    counts = Counter(o.layer for o in facts.overlays)
    multi = sorted(layer for layer, n in counts.items() if n > 1)
    if multi:
        flags.append(
            Flag(
                code="MULTI_DISTRICT",
                severity="info",
                message=(
                    "This parcel spans more than one district in: "
                    + ", ".join(multi)
                    + ". Rules from each may apply."
                ),
            )
        )

    return flags


def render_prompt_context(facts: ParcelFacts, flags: list[Flag]) -> str:
    """
    Serialize facts + flags into the block that goes into the LLM prompt.
    The wrapper text tells the model these values are authoritative.
    """
    payload = {
        "parcel_facts": facts.model_dump(mode="json"),
        "system_flags": [f.model_dump(mode="json") for f in flags],
    }
    return (
        "The following parcel facts were computed from city GIS data. They are "
        "authoritative. Do not change, recompute, or contradict them; explain them "
        "using only the ordinance excerpts provided.\n\n"
        + json.dumps(payload, indent=2, default=str)
    )


async def build_analysis_context(
    session: AsyncSession, parcel_id: int
) -> tuple[ParcelFacts, list[Flag], str] | None:
    """Convenience entry point for the service: facts, flags, and prompt block."""
    facts = await build_parcel_facts(session, parcel_id)
    if facts is None:
        return None
    flags = build_flags(facts)
    return facts, flags, render_prompt_context(facts, flags)


# app/ai/llm_client.py
"""
Thin wrapper around the Anthropic SDK.

Structured output is enforced with forced tool use: the model must call
`submit_analysis`, whose input schema is generated from AnalysisContent, and we
validate the tool input with Pydantic. SDK-level retries (connection errors,
429, 5xx) are handled by `max_retries`; we add one extra attempt only for
schema-validation failures.
"""
import logging

import anthropic
from pydantic import ValidationError

from app.ai.config import AIConfig
from app.ai.schemas import AnalysisContent

logger = logging.getLogger(__name__)

TOOL_NAME = "submit_analysis"
VALIDATION_ATTEMPTS = 2


class LLMError(Exception):
    """The provider failed or never returned a valid AnalysisContent."""


class LLMClient:
    def __init__(self, cfg: AIConfig) -> None:
        self._cfg = cfg
        self._client = anthropic.AsyncAnthropic(
            api_key=cfg.api_key,
            timeout=cfg.timeout_seconds,
            max_retries=2,
        )
        self._tool = {
            "name": TOOL_NAME,
            "description": "Submit the completed parcel zoning analysis.",
            "input_schema": AnalysisContent.model_json_schema(),
        }

    async def generate_analysis(self, *, system: str, user: str) -> AnalysisContent:
        last_error: Exception | None = None

        for attempt in range(1, VALIDATION_ATTEMPTS + 1):
            try:
                message = await self._client.messages.create(
                    model=self._cfg.model,
                    max_tokens=self._cfg.max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                    tools=[self._tool],
                    tool_choice={"type": "tool", "name": TOOL_NAME},
                )
            except anthropic.APIError as exc:
                logger.error("LLM provider error: %s", exc)
                raise LLMError(f"Provider error: {exc}") from exc

            logger.info(
                "LLM call ok: model=%s in=%s out=%s attempt=%s",
                self._cfg.model,
                message.usage.input_tokens,
                message.usage.output_tokens,
                attempt,
            )

            block = next((b for b in message.content if b.type == "tool_use"), None)
            if block is None:
                last_error = LLMError("Model returned no tool call")
                continue

            try:
                return AnalysisContent.model_validate(block.input)
            except ValidationError as exc:
                logger.warning("Analysis failed schema validation (attempt %s)", attempt)
                last_error = exc

        raise LLMError(f"No valid analysis after {VALIDATION_ATTEMPTS} attempts") from last_error