from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

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
    title: str = Field(min_length=2, max_length=140)
    subtitle: str = Field(min_length=2, max_length=180)
    description: str = Field(min_length=10, max_length=5000)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
