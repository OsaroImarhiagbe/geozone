# api/v1/router.py
from fastapi import APIRouter

# from app.modules.auth.api.v1.auth import router as auth_router
from app.service.health.api.v1.health import router as health_router
from app.service.parcels.api.v1.parcels import router as parcels_router

router = APIRouter()


# router.include_router(auth_router, prefix="/auth")
router.include_router(health_router,prefix="/health")
router.include_router(parcels_router,prefix="/parcels")