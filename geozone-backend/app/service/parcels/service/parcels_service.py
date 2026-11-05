from app.service.parcels.infrastructure.parcels.parcels_dal import ParcelsRepository
from app.service.parcels.schemas.zoning_schema import ParcelResponse, ParcelFeatureCollection
from fastapi import status

class ParcelsService:
    """
    Service handles zoning for the AOI
    """

    def __init__(self,repo: ParcelsRepository):
        self.__repo = repo

    async def parcels(self,min_lng: float,min_lat: float,max_lng: float,max_lat: float) -> ParcelResponse:
        """
        Service Layer Function for grabbing parcels based off the bounding box
        """
        response = await self.__repo.find_parcels_by_bbox(min_lng=min_lng,min_lat=min_lat,max_lng=max_lng,max_lat=max_lat)

        print("response:", response)
        return ParcelResponse(
            status=status.HTTP_200_OK,
            error="",
            data=ParcelFeatureCollection(
                type="FeatureCollection",
                features=response
            )
            )