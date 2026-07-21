from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

ITEM_TYPES = ("parcours", "competence", "realisation")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(Enum(*ITEM_TYPES, name="item_type"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), index=True, nullable=False, default="General")
    featured: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, default=False)
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
