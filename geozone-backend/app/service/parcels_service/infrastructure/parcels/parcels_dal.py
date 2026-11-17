from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, text

from geoalchemy2.functions import ST_Intersects, ST_MakeEnvelope

from app.service.parcels_service.infrastructure.models.parcels_table import Parcels
from app.service.parcels_service.schemas.parcel_schema import (ParcelFeature,ParcelQuery)

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
                            'parcel_id','pid', pid, 'address', address, 'zone_code', zone_code,
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

    async def get_parcel_by_id(self,parcel_id:str) -> str:


        sql = text("""

            SELECT parcel_id
            FROM parcels
            WHERE pid = :parcel_id
        """)

        result = await self.__db.execute(sql,{"pid":parcel_id})



        return result.scalar_one_or_none()

    async def get_parcel_metric(self,parcel_id:str):
        sql = text("""
                   SELECT
                        p.id,
                        p.zone_code,
                        ST_Area(p.geom) AS lot_area,
                        hd.name  AS height_district,
                        hist.name AS historic_district,
                        pk.name  AS parking_district
                        FROM parcels p
                        LEFT JOIN LATERAL (
                        SELECT name FROM height_districts h
                        WHERE ST_Intersects(h.geom, p.geom)
                        LIMIT 1
                        ) hd ON true
                        LEFT JOIN LATERAL (
                        SELECT name FROM historic_districts h
                        WHERE ST_Intersects(h.geom, p.geom)
                        LIMIT 1
                        ) hist ON true
                        LEFT JOIN LATERAL (
                        SELECT name FROM parking_districts k
                        WHERE ST_Intersects(k.geom, p.geom)
                        LIMIT 1
                        ) pk ON true
                        WHERE p.id = :parcel_id;
                   """)
        result = await self.__db.execute(sql,{"pid":parcel_id})

        return result.scalar_one_or_none()
        
        