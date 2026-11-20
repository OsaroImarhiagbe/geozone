from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Query
from typing import Annotated


from app.service.analysis_service.service.analysis import AnalysisService
from app.service.analysis_service.api.dependencies.dependencies import get_auth_analysis_service

from fastapi import APIRouter, Depends, HTTPException
from app.service.analysis_service.schemas.analysis_schema import (AnalysisRequest, GenerateRequest, GenerateResponse)

# app/api/v1/analysis.py
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.config import AIConfig
from app.ai.llm_client import LLMClient
from app.service.analysis_service.schemas.analysis_schema import (AnalysisRequest, AnalysisResponse, ErrorResponse)


router = APIRouter(tags=["analysis"])


# @lru_cache
# def get_ai_config() -> AIConfig:
#     return AIConfig()


# @lru_cache
# def get_llm_client() -> LLMClient:
#     # One client per process: reuses the HTTP connection pool
#     return LLMClient(get_ai_config())


# To Do: Finish out refresh token endpoint and register user endpoint

# filter_query: Annotated[ParcelQuery, Query()]
get_analysis_service_dependency = Annotated[AnalysisService, Depends(get_auth_analysis_service)]

@router.post('/parcels')
async def generate_analysis(
    request:AnalysisRequest,
    analysis_service: get_analysis_service_dependency):
    """
    Endpoint is getting parcels zones based on bounding area
    """
    try:
      # send parcel_id to analysis service
      data = await analysis_service.generate_analysis_by_parcel_id(parcel=request)
      return
      # return ParcelResponse(
      #    status=status.HTTP_200_OK,
      #    error=None,
      #    data=data
      # )
    except ValueError as e:
      raise HTTPException(
       status_code=status.HTTP_404_NOT_FOUND,
       detail=str(e)
      )
    except RuntimeError:
       raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="Internal Server Error"
       )

@router.post("/parcels/{parcel_id}/analysis",response_model=AnalysisResponse,responses={404: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},)
async def analyze_parcel(
    parcel_id: int,
    body: AnalysisRequest | None = None,
    _user=Depends(get_current_user),  # auth gate; analysis itself is not user-scoped
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResponse:
    persona = (body or AnalysisRequest()).persona

    try:
        result = await service.analyze(parcel_id, persona)
    except AnalysisGenerationError:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "llm_unavailable",
                "message": "The analysis service is temporarily unavailable. Try again shortly.",
                "retry_after": 30,
            },
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "parcel_not_found", "message": "Parcel not found."},
        )
    return result
