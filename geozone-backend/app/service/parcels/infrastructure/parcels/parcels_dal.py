from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, text

from geoalchemy2.functions import ST_Intersects, ST_MakeEnvelope

from app.service.parcels.infrastructure.models.parcels_table import Parcels
from app.service.parcels.schemas.parcel_schema import (ParcelFeature,ParcelQuery)

from pprint import pprint

import json

class ParcelsRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db
        
    async def get_parcels_geojson(self, bbox: ParcelQuery, limit: int = 20000) -> str:
        where = (
            "WHERE geometry && ST_MakeEnvelope(:min_lng, :min_lat, :max_lng, :max_lat, 4326)"
            if bbox.has_bbox else ""
        )
        sql = text(f"""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'name', 'RealEstate_Parcels',
                'features', COALESCE(json_agg(f.feature), '[]'::json)
            )::text
            FROM (
                SELECT DISTINCT ON (md5(ST_AsBinary(geometry)))
                    json_build_object(
                        'type', 'Feature',
                        'properties', json_build_object(
                            'pid', pid, 'address', address, 'zone_code', zone_code,
                            'land_desc', land_desc, 'land_sf', land_sf
                        ),
                        'geometry', ST_AsGeoJSON(geometry, 6)::json
                    ) AS feature
                FROM parcels
                {where}
                ORDER BY md5(ST_AsBinary(geometry))
                LIMIT :limit
            ) f
        """)
        params = {"limit": limit}
        if bbox.has_bbox:
            params.update(bbox.model_dump())
        result = await self.__db.execute(sql, params)
        return result.scalar_one()