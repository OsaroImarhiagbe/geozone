from app.service.parcels.infrastructure.parcels.parcels_dal import ParcelsRepository
from app.service.parcels.schemas.parcel_schema import (ParcelFeature, ParcelFeatureCollection,ParcelProperties,ParcelQuery)

from fastapi import status

from pprint import pprint

class ParcelsService:
    """
    Service handles zoning for the AOI
    """

    def __init__(self,repo: ParcelsRepository):
        self.__repo = repo

    async def get_parcels(self,bbox:ParcelQuery) -> str:
        """
        Service Layer Function for grabbing parcels based off the bounding box
        """
        features = await self.__repo.get_parcels_geojson(bbox)

        if not features:
            raise ValueError

        
        return features

    # ParcelFeatureCollection(
    #             type="FeatureCollection",
    #             name="RealEstate_Parcels",
    #             features=features
    #         )