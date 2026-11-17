from app.service.parcels_service.infrastructure.parcels.parcels_dal import ParcelsRepository
from app.service.parcels_service.schemas.parcel_schema import (ParcelQuery,ParcelIdStr)

from fastapi import status

from pprint import pprint

class ParcelsService:
    """
    Service handles zoning for the AOI
    """

    def __init__(self,repo: ParcelsRepository):
        self.__repo = repo

    async def getParcels(self,bbox:ParcelQuery) -> str:
        """
        Service Layer Function for grabbing parcels based off the bounding box
        """
        features = await self.__repo.get_parcels_geojson(bbox)

        if not features:
            raise ValueError("Feature not found")

            # ParcelFeatureCollection(
    #             type="FeatureCollection",
    #             name="RealEstate_Parcels",
    #             features=features
    #         )
        
        return features

    async def get_parcel_by_id(self,parcel_id:str):
        """
        Service layer function to grab a parcel by the its pid (parcel_id)
        """

        if not ParcelIdStr(parcel_id=parcel_id):
            raise ValueError(f"{parcel_id} is invlaid format")
        # Add a logger here

        # grab the parcel by the id and return it
        parcelId = await self.__repo.get_parcel_by_id(parcel_id)

        if parcelId is None:
            raise ValueError(f"{parcel_id} not found!")
        ## I think add a logger here

        return parcelId

    async def get_parcel_metrics(self,parcel_id:str):

        # step 1: grab the parcel by the
        parcelID = await self.get_parcel_by_id(parcel_id=parcel_id)

        #step 2: grab zoning,heights, historic,and parking metrics compare them with parcel coorindates
        metric = await self.__repo.get_parcel_metric(parcel_id=parcelID)

        # step 3: transform result into correct data format
        if metric is None:
            raise ValueError(f"{parcel_id} metric could not be compunded!")

        # loop over result and transform

        