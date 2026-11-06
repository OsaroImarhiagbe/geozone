from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.dependecies import ( get_anon_db, get_auth_db)
from app.service.parcels.infrastructure.parcels.parcels_dal import ParcelsRepository
from app.service.parcels.service.parcels_service import ParcelsService
from app.middleware.dependencies import get_authenticated_user



def build_parcels_service(db: AsyncSession) -> ParcelsService:
    repo = ParcelsRepository(db)
    service = ParcelsService(repo)
    return service


def get_anon_parcels_service(db: Annotated[AsyncSession, Depends(get_anon_db)]) -> ParcelsService:
    return build_parcels_service(db)

def get_auth_parcels_service(db: Annotated[AsyncSession, Depends(get_auth_db)]) -> ParcelsService:
    return build_parcels_service(db)

# AnonParcelsService = Annotated[ParcelsService,Depends(get_anon_parcels_service)]

# AuthParcelsService = Annotated[ParcelsService,Depends(get_auth_parcels_service)]

async def get_parcels_service(current_user = Depends(get_authenticated_user)) -> AsyncGenerator[ParcelsService, None]:

    if current_user:
        db_generator = get_auth_db()
    else:
        db_generator = get_anon_db()

    async for db in db_generator:
        yield build_parcels_service(db)
