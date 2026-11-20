from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Query
from typing import Annotated
from app.service.parcels_service.schemas.parcel_schema import (ParcelQuery, ParcelResponse)
from app.service.parcels_service.service.parcels import ParcelsService
from app.service.parcels_service.service.dependencies import get_anon_parcels_service


router = APIRouter(tags=["parcels"])

#`GET /api/zoning/parcels?min_lng=-77.12&min_lat=38.78&max_lng=-77.01&max_lat=38.85`
## client is passing current mapbox bounding arrays as parameters
# What the response looks like {
###"type": "FeatureCollection",
'''"features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[...]]
      },
      "properties": {
        "parcel_id": "123abc",
        "zone_code": "CC",
        "description": "Commercial Community"
      }
    }
  ]
}'''




# To Do: Finish out refresh token endpoint and register user endpoint

# filter_query: Annotated[ParcelQuery, Query()]
get_parcels_service_dependency = Annotated[ParcelsService, Depends(get_anon_parcels_service)]

@router.get('/bbox')
async def get_zones(service: get_parcels_service_dependency, query: Annotated[ParcelQuery, Query()],)-> Response:
    """
    Endpoint is getting parcels zones based on bounding area
    """
    try:
        
      data = await service.getParcels(query)
      return data
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