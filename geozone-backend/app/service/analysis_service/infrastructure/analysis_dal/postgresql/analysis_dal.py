from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



# from redis.exceptions import RedisError
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert


from app.service.analysis_service.infrastructure.models.parcel_analysis import ParcelAnalysis
from app.service.analysis_service.schemas.analysis_schema import(
    AnalysisContent,
    AnalysisMeta,
    AnalysisResponse,
    DataFreshness,
    Flag,
    ParcelFacts,
    Persona,
)



class AnalysisRepository:
    """
            Data access layer for AI analyses.

            Read path : Redis -> Postgres (re-warm Redis on a DB hit) -> None
            Write path: Postgres upsert (source of truth) -> Redis SETEX (best effort)

            Redis is a cache only. A Redis failure must never fail the request.
"""
    def __init__(self,db:AsyncSession):
        self.__db = db
        
    async def save_analysis(self,redis: Redis,response: AnalysisResponse) -> AnalysisResponse:
            """
            Upsert the analysis into Postgres, then write it through to Redis.

            Upsert (not plain insert) so two concurrent first requests for the same
            parcel/persona don't fail on the unique constraint; last write wins.
            The DB commit happens BEFORE the cache write so Redis never holds data
            that was rolled back.
                    """
            meta = response.meta

            values = {
                "parcel_id": response.facts.parcel_id,
                "persona": meta.persona.value,
                "ordinance_version": meta.ordinance_version,
                "prompt_version": meta.prompt_version,
                "model": meta.model,
                "status": response.status,
                "facts": response.facts.model_dump(mode="json"),
                "flags": [f.model_dump(mode="json") for f in response.flags],
                "analysis": (
                    response.analysis.model_dump(mode="json") if response.analysis else None
                ),
                "data_freshness": [d.model_dump(mode="json") for d in meta.data_freshness],
                "generated_at": meta.generated_at,
            }

            stmt = pg_insert(ParcelAnalysis).values(**values)
            stmt = stmt.on_conflict_do_update(
                constraint="uq_parcel_analysis_variant",
                set_={
                    "model": stmt.excluded.model,
                    "status": stmt.excluded.status,
                    "facts": stmt.excluded.facts,
                    "flags": stmt.excluded.flags,
                    "analysis": stmt.excluded.analysis,
                    "data_freshness": stmt.excluded.data_freshness,
                    "generated_at": stmt.excluded.generated_at,
                },
            )

            await session.execute(stmt)
            await session.commit()

            key = cache_key(
                values["parcel_id"], values["persona"],
                values["ordinance_version"], values["prompt_version"],
            )
            await _cache_set(redis, key, response)
            return response
    
    async def get_analysis(self,redis: Redis,*,parcel_id: int,persona: Persona,ordinance_version: str,prompt_version: str,) -> AnalysisResponse | None:
        """Redis first, then Postgres. Re-warms Redis on a DB hit."""
        key = cache_key(parcel_id, persona.value, ordinance_version, prompt_version)

        hit = await _cache_get(redis, key)
        if hit is not None:
            return _mark_cached(hit)

        row = (
            await session.execute(
                select(ParcelAnalysis).where(
                    ParcelAnalysis.parcel_id == parcel_id,
                    ParcelAnalysis.persona == persona.value,
                    ParcelAnalysis.ordinance_version == ordinance_version,
                    ParcelAnalysis.prompt_version == prompt_version,
                )
            )
        ).scalar_one_or_none()

        if row is None:
            return None

        response = _row_to_response(row, cached=False)
        await _cache_set(redis, key, response)
        return _mark_cached(response)
    













# --------------------------------------------------------------------------
# Row <-> response mapping
# --------------------------------------------------------------------------
def _row_to_response(row: ParcelAnalysis, *, cached: bool) -> AnalysisResponse:
    return AnalysisResponse(
        status=row.status,
        facts=ParcelFacts.model_validate(row.facts),
        flags=[Flag.model_validate(f) for f in row.flags],
        analysis=AnalysisContent.model_validate(row.analysis) if row.analysis else None,
        meta=AnalysisMeta(
            cached=cached,
            generated_at=row.generated_at,
            persona=Persona(row.persona),
            model=row.model,
            prompt_version=row.prompt_version,
            ordinance_version=row.ordinance_version,
            data_freshness=[DataFreshness.model_validate(d) for d in row.data_freshness],
        ),
    )


def _mark_cached(response: AnalysisResponse) -> AnalysisResponse:
    response.meta = response.meta.model_copy(update={"cached": True})
    return response






