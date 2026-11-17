from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, String, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from app.infrastructure.db.base_models.base import Base


class Zoning(Base):

    __tablename__ = "zoning"
    zoning_id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    ordinance:Mapped[int] = mapped_column(nullable=True,unique=False,comment="ordinance number of zone")
    instrument:Mapped[str] = mapped_column(String(100),unique=False, nullable=True,comment="instrument")
    geometry:Mapped[Geometry] = mapped_column(Geometry(geometry_type="MULTIPOLYGON", srid=4326),comment="polygon geometry")
    shape_area:Mapped[float] = mapped_column(Float, unique=False, nullable=True,comment="shape area")
    shape_length:Mapped[float] = mapped_column(Float, unique=False, nullable=True,comment="shape length")
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),doc="Create At",comment="When the user was first created")
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now(),doc="Updated At",comment="When the user was updated")
    last_synced:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now(),doc="Last Login",comment="User's last login attempt")