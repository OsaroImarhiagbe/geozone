
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.dependecies import ( get_anon_db, get_auth_db)
from app.service.analysis_service.infrastructure.analysis_dal.analysis_dal import AnalysisRepository
from app.service.analysis_service.service.analysis import AnalysisService
from app.service.parcels_service.service.parcels import ParcelsService


# @lru_cache
# def get_llm_gateway() -> LlmGateway:
#     return LlmGateway(
#         providers={
#             "anthropic": AnthropicAdapter(api_key=os.environ["ANTHROPIC_API_KEY"]),
#             "openai": OpenAiAdapter(api_key=os.environ["OPENAI_API_KEY"]),
#         },
#         default_provider="anthropic",
#     )





def build_analysis_service(db: AsyncSession) -> AnalysisService:
    repo = AnalysisRepository(db)
    parcel_service = ParcelsService(db)
    analysis_service = AnalysisService(repo,parcel_service)
    return analysis_service


# def get_anon_analyzer_service(db: Annotated[AsyncSession, Depends(get_anon_db)]) -> AnalyzerService:
#     return build_ai_service(db)

def get_auth_analysis_service(db: Annotated[AsyncSession, Depends(get_auth_db)]) -> AnalysisService:
    return build_analysis_service(db)

# AnonParcelsService = Annotated[ParcelsService,Depends(get_anon_parcels_service)]

# AuthParcelsService = Annotated[ParcelsService,Depends(get_auth_parcels_service)]

# async def get_analyzer_service(current_user = Depends(get_authenticated_user)) -> AsyncGenerator[AnalyzerService, None]:

#     if current_user:
#         db_generator = get_auth_db()
#     else:
#         db_generator = get_anon_db()

#     return build_ai_service(db_generator)

