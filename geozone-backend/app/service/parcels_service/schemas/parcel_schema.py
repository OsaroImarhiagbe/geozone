from pydantic import BaseModel
from typing import Literal,Optional,Annotated
from pydantic import BaseModel,Field, ConfigDict

ParcelIdStr = Annotated[str, Field(pattern=r"^\d{3}\.\d{2}-\d{2}-\d{2}(?:\.\d+)?$")]


class ParcelIDParameter(BaseModel):
    parcel_id:ParcelIdStr

    
class ParcelQuery(BaseModel):
    min_lng: float | None = None
    min_lat: float | None = None
    max_lng: float | None = None
    max_lat: float | None = None

    @property
    def has_bbox(self) -> bool:
        return None not in (self.min_lng, self.min_lat, self.max_lng, self.max_lat)



class PolygonGeometry(BaseModel):
    type: Literal["Polygon"]
    coordinates: list[list[list[float]]]  # [[[lng, lat], [lng, lat], ...]]


class MultiPolygonGeometry(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: list[list[list[list[float]]]]


ParcelGeometry = Annotated[
    PolygonGeometry | MultiPolygonGeometry, Field(discriminator="type")
]


class ParcelProperties(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    objectid:int | None = None
    parceltype: str | None = None
    pid:str | None = None
    map:str | None = None
    block:str | None = None
    lot_gis:str | None = None
    lot_re:str  | None = None
    account_number:str  | None = None
    address:str | None = None 
    st_num:str | None = None
    st_alpha:str  | None = None
    st_name:str | None = None
    st_type:str | None = None 
    unit:str | None = None 
    plat:str | None = None 
    legal_lot:str | None = None 
    status:str | None = None 
    land_code:str | None = None 
    land_desc:str | None = None 
    prp_name:str | None = None
    zone_code:str | None = None 
    neighborho:str| None = None 
    land_sf:float | None = None 
    own_name:str | None = None 
    owner_name_2:str | None = None
    own_add:str | None = None 
    own_add_2:str | None = None 
    own_city:str | None = None
    own_stat:str | None = None
    own_zip:str | None = None 
    instrument:str | None = None


class ParcelFeature(BaseModel):
    type: Literal["Feature"]
    properties: ParcelProperties
    geometry: ParcelGeometry
   


class ParcelFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    name:str
    features: list[ParcelFeature]

class ParcelResponse(BaseModel):
    status:int
    error:str | None = None
    data: ParcelFeatureCollection


class ParcelOverlayRow(BaseModel):
    """One row returned by the parcel + overlay lookup query."""

    model_config = ConfigDict(from_attributes=True)

    id: int                              # p.id (never null: it's the WHERE key)
    zone_code: str | None = None         # p.zone_code
    lot_area: float | None = None        # ST_Area(p.geom)
    height_district: str | None = None   # hd.name, NULL if no intersecting polygon
    historic_district: str | None = None # hist.name, NULL if no intersecting polygon
    parking_district: str | None = None  # pk.name, NULL if no intersecting polygon