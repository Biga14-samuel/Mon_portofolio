from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, UniqueConstraint, func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

ITEM_TYPES = ("parcours", "competence", "realisation", "blog")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(Enum(*ITEM_TYPES, name="item_type"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), index=True, nullable=False, default="General")
    featured: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, default=False)
    display_order: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    demo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    content: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("type", "name", name="uq_tags_type_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Testimonial(Base):
    __tablename__ = "testimonials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_name: Mapped[str] = mapped_column(String(140), nullable=False)
    client_company: Mapped[str | None] = mapped_column(String(140), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
