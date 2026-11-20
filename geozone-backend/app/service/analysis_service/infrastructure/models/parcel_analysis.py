# app/analysis/models.py
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_models.base import Base


class ParcelAnalysis(Base):
    """
    One stored AI analysis per (parcel, persona, ordinance version, prompt version).

    The same four-part key is used for the Redis cache key, so a prompt or
    ordinance update naturally invalidates old rows instead of serving stale text.

    The analysis is shared across users (it describes the parcel, not the user),
    so it is NOT user-scoped and does not need row-level security.
    """

    __tablename__ = "parcel_analyses"
    __table_args__ = (
        UniqueConstraint(
            "parcel_id",
            "persona",
            "ordinance_version",
            "prompt_version",
            name="uq_parcel_analysis_variant",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # NOTE: match the type of parcels.id (BigInteger assumed)
    parcel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("parcels.parcel_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Variant key
    persona: Mapped[str] = mapped_column(String(32), nullable=False)
    ordinance_version: Mapped[str] = mapped_column(String(32), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(32), nullable=False)

    # Generation info
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # ok | partial | insufficient_data

    # Payload, stored as the validated Pydantic dumps
    facts: Mapped[dict] = mapped_column(JSONB, nullable=False)
    flags: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    data_freshness: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )