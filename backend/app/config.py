from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_expire_minutes: int = 60
    admin_username: str
    admin_password_hash: str
    cors_origins: str = "http://localhost:5173,https://mon-portofolio-phi.vercel.app,https://biga14-samuel.github.io"
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_recipient: str = "samuelbiga10@gmail.com"
    sendgrid_api_key: str | None = None
    supabase_url: str | None = None
    supabase_key: str | None = None
    supabase_bucket: str = "portfolio-uploads"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("smtp_server", "smtp_user", "smtp_recipient", mode="before")
    @classmethod
    def strip_smtp_strings(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("smtp_password", mode="before")
    @classmethod
    def normalize_smtp_password(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return "".join(value.split())

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
