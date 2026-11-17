from app.service.analysis_service.infrastructure.analysis_dal.analysis_dal import AnalysisRepository
from app.service.parcels_service.service.parcels import ParcelsService
from app.service.analysis_service.infrastructure.ai_infrastructure.anthropic.anthropic_adapter import AnthropicAdapter

from app.service.parcels_service.schemas.parcel_schema import ParcelIdStr

from app.service.analysis_service.schemas.analysis_schema import AnalysisRequest

class AnalysisService:
    """ Serivce handles calling Claude API for AI Analysis"""
    
    def __init__(self,repo:AnalysisRepository,parcel_service:ParcelsService):
        self.__repo = repo
        self.__parcel_service = parcel_service
        self.__ai = AnthropicAdapter

    async def generate_analysis_by_parcel_id(self,parcel:AnalysisRequest):
        """
        Service layer function makes external API call to Claude LLM API
        """
        # if parcel id is not valid raise error
        if not ParcelIdStr(parcel_id=parcel.pid):
            return ValueError(f"{parcel.pid} is not a valid format")
        # we can add a logger here

        result = await self.__parcel_service.get_parcel_metrics(parcel_id=parcel.pid)

