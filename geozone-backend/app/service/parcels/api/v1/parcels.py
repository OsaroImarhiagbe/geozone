from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Query
from typing import Annotated
from app.service.parcels.schemas.zoning_schema import ZoningQuery
from app.service.parcels.service.parcels_service import ParcelsService
from app.service.parcels.service.dependencies import get_parcels_service
from app.service.parcels.schemas.zoning_schema import ParcelResponse
router = APIRouter(tags=["zoning"])

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


get_parcels_service_dependency = Annotated[ParcelsService, Depends(get_parcels_service)]

@router.get('/',response_model=ParcelResponse,tags=['parcels'])
async def get_zones(service: get_parcels_service_dependency, filter_query: Annotated[ZoningQuery, Query()]) -> ParcelResponse:
    """
    Endpoint is getting parcels zones based on bounding area
    """
    try:
        
      response = await service.parcels(min_lng=filter_query.min_lng,min_lat=filter_query.min_lat,max_lng=filter_query.max_lng,max_lat=filter_query.max_lat)
      return response
    except LookupError as e:
      return HTTPException(
       status_code=status.HTTP_404_NOT_FOUND,
       detail=str(e)
      )
    except RuntimeError:
       return HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="Internal Server Error"
       )