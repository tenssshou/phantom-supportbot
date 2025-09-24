from pydantic import BaseSettings, Field, PostgresDsn, validator
from typing import Optional


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_CHAT_ID: int
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_URL: Optional[str] = None
    DATABASE_URL: PostgresDsn
    HOST: str = "0.0.0.0"
    PORT: int = 3000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("WEBHOOK_URL", pre=True, always=True)
    def assemble_webhook_url(cls, v, values):
        if v:
            return v
        host = values.get("WEBHOOK_HOST")
        path = values.get("WEBHOOK_PATH", "/webhook")
        token = values.get("BOT_TOKEN")
        return f"{host}{path}/{token}"


settings = Settings()
