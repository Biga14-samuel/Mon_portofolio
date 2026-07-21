from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ItemType = Literal["parcours", "competence", "realisation"]


class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=8, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ItemBase(BaseModel):
    type: ItemType
    category: str = Field(min_length=2, max_length=80)
    featured: bool = False
    display_order: int = Field(default=0, ge=0, le=100000)
    title: str = Field(min_length=2, max_length=140)
    subtitle: str = Field(min_length=2, max_length=180)
    description: str = Field(min_length=10, max_length=5000)
    github_url: str | None = Field(default=None, max_length=500)
    demo_url: str | None = Field(default=None, max_length=500)
    image_url: str | None = Field(default=None, max_length=500)
    content: dict | None = Field(default=None)

    @field_validator("github_url", "demo_url", "image_url", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    type: ItemType
    name: str = Field(min_length=2, max_length=80)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
