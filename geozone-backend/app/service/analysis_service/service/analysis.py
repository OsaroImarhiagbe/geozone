from app.service.analysis_service.infrastructure.analysis_dal.postgresql.analysis_dal import AnalysisRepository
from app.service.parcels_service.service.parcels import ParcelsService
from app.service.analysis_service.infrastructure.ai_infrastructure.anthropic.anthropic_adapter import AnthropicAdapter

from app.service.parcels_service.schemas.parcel_schema import ParcelIdStr

from app.service.analysis_service.schemas.analysis_schema import AnalysisRequest


import logging
from datetime import datetime, timezone


from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.config import AIConfig
from app.ai.context_builder import build_analysis_context
from app.service.analysis_service.infrastructure.analysis_dal.postgresql.analysis_dal import AnalysisRepository
from app.ai.llm_client import LLMClient, LLMError
from app.ai.prompt_builder import build_prompts
from app.ai.retriever import retrieve_sections
from app.service.analysis_service.schemas.analysis_schema import (
    AnalysisContent,
    AnalysisMeta,
    AnalysisResponse,
    DataFreshness,
    Flag,
    ParcelFacts,
    Persona,
)
from app.ai.validator import ground_content

logger = logging.getLogger(__name__)


# class AnalysisGenerationError(Exception):
#     """The LLM step failed. The router maps this to a 502."""


class AnalysisService:
    """
        Orchestrates the full analysis flow:

        cache/DB hit? -> return
        build facts + flags (PostGIS)
        retrieve ordinance sections
        no sections?  -> insufficient_data (NOT cached, so it self-heals once text is loaded)
        LLM call -> schema-validated AnalysisContent
        ground against retrieved sections (drop unsupported claims)
        save (Postgres upsert + Redis) -> return
        """
    
    def __init__(
        self,
        repo:AnalysisRepository,
        parcel_service:ParcelsService,
    ):
        self.__repo = repo
        self.__parcel_service = parcel_service
        self.__ai = AnthropicAdapter
        self.llm = llm
        self.cfg = cfg

    async def generate_analysis_by_parcel_id(self,parcel:AnalysisRequest):
        """
        Service layer function makes external API call to Claude LLM API
        """
        # step 1: if parcel id is not valid raise error
        if not ParcelIdStr(parcel_id=parcel.pid):
            return ValueError(f"{parcel.pid} is not a valid format")
        # we can add a logger here

        # step 2: call parcel service to get the metrics of the parcel based on parcel id
        result = await self.__parcel_service.get_parcel_metrics(parcel_id=parcel.pid)

        # step 3:
    
    # async def analyze(self, parcel_id: int, persona: Persona) -> AnalysisResponse | None:
    #     """Return the analysis, or None if the parcel doesn't exist."""
    #     # 1. Redis -> Postgres
    #     cached = await get_analysis(
    #         self.session,
    #         self.redis,
    #         parcel_id=parcel_id,
    #         persona=persona,
    #         ordinance_version=self.cfg.ordinance_version,
    #         prompt_version=self.cfg.prompt_version,
    #     )
    #     if cached is not None:
    #         return cached

    #     # 2. Deterministic facts and flags
    #     ctx = await build_analysis_context(self.session, parcel_id)
    #     if ctx is None:
    #         return None
    #     facts, flags, context_block = ctx
    #     freshness = await self._data_freshness()

    #     # 3. Ordinance text
    #     sections = await retrieve_sections(self.session, facts, self.cfg)
    #     if not sections:
    #         logger.warning(
    #             "No ordinance text for parcel %s (zone=%s)", parcel_id, facts.zone_code
    #         )
    #         return self._insufficient(facts, flags, persona, freshness)

    #     # 4. LLM
    #     system, user = build_prompts(context_block, sections, persona)
    #     try:
    #         content = await self.llm.generate_analysis(system=system, user=user)
    #     except LLMError as exc:
    #         raise AnalysisGenerationError(str(exc)) from exc

    #     # 5. Grounding check
    #     content, dropped = ground_content(content, sections)
    #     if not content.citations:
    #         # Nothing survived verification: don't present ungrounded narrative
    #         logger.error("Parcel %s: no valid citations survived grounding", parcel_id)
    #         return self._insufficient(facts, flags, persona, freshness)

    #     status = "partial" if dropped else "ok"

    #     # 6. Persist (DB first, then Redis)
    #     response = self._build_response(
    #         status, facts, flags, content, persona, freshness
    #     )
    #     return await save_analysis(self.session, self.redis, response)
    
    # def _build_response(self,status: str,facts: ParcelFacts,flags: list[Flag],analysis: AnalysisContent | None,persona: Persona,freshness: list[DataFreshness],) -> AnalysisResponse:
    #     return AnalysisResponse(
    #         status=status,
    #         facts=facts,
    #         flags=flags,
    #         analysis=analysis,
    #         meta=AnalysisMeta(
    #             cached=False,
    #             generated_at=datetime.now(timezone.utc),
    #             persona=persona,
    #             model=self.cfg.model,
    #             prompt_version=self.cfg.prompt_version,
    #             ordinance_version=self.cfg.ordinance_version,
    #             data_freshness=freshness,
    #         ),
    #     )
    #     # ------------------------------------------------------------------
    # def _insufficient(self,facts: ParcelFacts,flags: list[Flag],persona: Persona,freshness: list[DataFreshness],) -> AnalysisResponse:
    #     flags = [
    #         *flags,
    #         Flag(
    #             code="NO_ORDINANCE_TEXT",
    #             severity="info",
    #             message=(
    #                 "We couldn't generate a reliable analysis for this parcel's zone. "
    #                 "The parcel details and warnings above are still accurate."
    #             ),
    #         ),
    #     ]
    #     return self._build_response(
    #         "insufficient_data", facts, flags, None, persona, freshness
    #     )


    # async def _data_freshness(self) -> list[DataFreshness]:
    #     rows = (
    #         (
    #             await self.session.execute(
    #                 text("SELECT dataset, source_updated_at FROM dataset_versions")
    #             )
    #         )
    #         .mappings()
    #         .all()
    #     )
    #     return [
    #         DataFreshness(dataset=r["dataset"], source_updated_at=r["source_updated_at"])
    #         for r in rows
    #     ]


    # app/ai/retriever.py
    # """
    # MVP retriever: exact key lookup, no embeddings.

    # Sections are fetched by the parcel's zone code and by the topics implied by its
    # overlays. Later you can add pgvector behind this same function for free-form
    # questions without touching the rest of the pipeline.

    # Assumed table (loaded offline by your ingestion script):

    #     CREATE TABLE ordinance_sections (
    #     id                bigserial PRIMARY KEY,
    #     ordinance_version text   NOT NULL,
    #     section_number    text   NOT NULL,
    #     title             text,
    #     text              text   NOT NULL,
    #     zone_codes        text[] NOT NULL DEFAULT '{}',  -- e.g. {'R-8','R-12'}
    #     topics            text[] NOT NULL DEFAULT '{}',  -- e.g. {'historic'}, {'height'}
    #     url               text,
    #     UNIQUE (ordinance_version, section_number)
    #     );
    #     CREATE INDEX ON ordinance_sections USING gin (zone_codes);
    #     CREATE INDEX ON ordinance_sections USING gin (topics);
    # """
    # import logging

    # from pydantic import BaseModel
    # from sqlalchemy import text
    # from sqlalchemy.ext.asyncio import AsyncSession

    # from app.ai.config import AIConfig
    # from app.ai.schemas import ParcelFacts

    # logger = logging.getLogger(__name__)

    # # overlay layer -> ordinance topic tag
    # OVERLAY_TOPICS = {
    #     "height": "height",
    #     "historic": "historic",
    #     "parking": "parking",
    #     "paid_parking": "parking",
    # }


    # class OrdinanceSection(BaseModel):
    #     section_number: str
    #     title: str | None = None
    #     text: str
    #     url: str | None = None


    # def normalize_zone(code: str | None) -> str | None:
    #     """Normalize so 'R-8 ' and 'r-8' match what ingestion stored.
    #     Extend this if your layer codes differ from the ordinance (e.g. 'OCM(50)')."""
    #     return code.strip().upper() if code else None


    # _SQL = text(
    #     """
    #     SELECT section_number, title, text, url,
    #         (zone_codes && CAST(:zones AS text[])) AS is_zone_match
    #     FROM ordinance_sections
    #     WHERE ordinance_version = :version
    #     AND (zone_codes && CAST(:zones AS text[])
    #         OR topics && CAST(:topics AS text[]))
    #     ORDER BY is_zone_match DESC, section_number
    #     """
    # )


    # async def retrieve_sections(
    #     session: AsyncSession, facts: ParcelFacts, cfg: AIConfig
    # ) -> list[OrdinanceSection]:
    #     zone = normalize_zone(facts.zone_code)
    #     zones = [zone] if zone else []
    #     topics = sorted({OVERLAY_TOPICS[o.layer] for o in facts.overlays})

    #     if not zones and not topics:
    #         return []

    #     rows = (
    #         (
    #             await session.execute(
    #                 _SQL,
    #                 {
    #                     "version": cfg.ordinance_version,
    #                     "zones": zones,
    #                     "topics": topics,
    #                 },
    #             )
    #         )
    #         .mappings()
    #         .all()
    #     )

    #     # Zone sections come first (ORDER BY), so truncation drops overlay text last.
    #     sections: list[OrdinanceSection] = []
    #     used = 0
    #     for r in rows:
    #         size = len(r["text"])
    #         if used + size > cfg.ordinance_char_budget:
    #             logger.warning(
    #                 "Ordinance budget reached for parcel %s; dropped section %s",
    #                 facts.parcel_id,
    #                 r["section_number"],
    #             )
    #             continue
    #         used += size
    #         sections.append(
    #             OrdinanceSection(
    #                 section_number=r["section_number"],
    #                 title=r["title"],
    #                 text=r["text"],
    #                 url=r["url"],
    #             )
    #         )
    #     return sections
