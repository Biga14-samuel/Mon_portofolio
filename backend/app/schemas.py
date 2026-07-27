from datetime import datetime
from typing import Literal
import nh3

from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr

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


class TestimonialBase(BaseModel):
    client_name: str = Field(min_length=2, max_length=140)
    client_company: str | None = Field(default=None, max_length=140)
    linkedin_url: str | None = Field(default=None, max_length=500)
    content: str = Field(min_length=5, max_length=2000)

    @field_validator("client_company", "linkedin_url", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("content", "client_name", "client_company", mode="after")
    @classmethod
    def sanitize_html(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            # nh3.clean supprime toutes les balises HTML dangereuses (protection XSS)
            return nh3.clean(value)
        return value

class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    is_visible: bool


class TestimonialRead(TestimonialBase):
    id: int
    is_visible: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactRequest(BaseModel):
    email: EmailStr = Field(max_length=150)
    subject: str | None = Field(default=None, max_length=150)
    message: str = Field(min_length=10, max_length=3000)

    @field_validator("subject", "message", mode="after")
    @classmethod
    def sanitize_html(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return nh3.clean(value)
        return value

