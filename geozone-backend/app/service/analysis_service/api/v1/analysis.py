from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Query
from typing import Annotated


from app.service.analysis_service.service.analysis import AnalysisService
from app.service.analysis_service.api.dependencies.dependencies import get_auth_analysis_service

from fastapi import APIRouter, Depends, HTTPException
from app.service.analysis_service.schemas.analysis_schema import (AnalysisRequest, GenerateRequest, GenerateResponse)


router = APIRouter(tags=["parcel_analyzer"])




# To Do: Finish out refresh token endpoint and register user endpoint

# filter_query: Annotated[ParcelQuery, Query()]
get_analysis_service_dependency = Annotated[AnalysisService, Depends(get_auth_analysis_service)]

@router.post('/parcels/analysis')
async def generate_analysis(request:AnalysisRequest,analysis_service: get_analysis_service_dependency):
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



# @router.post("/generate", response_model=GenerateResponse)
# async def generate_completion(request: GenerateRequest,gateway: LlmGateway = Depends(get_llm_gateway),) -> GenerateResponse:
#     try:
#         return await gateway.generate(request)
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc))
