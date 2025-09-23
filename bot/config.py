from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_GROUP_ID: int
    ADMIN_USER_IDS: List[int]

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    WEBHOOK_URL: str
    WEBHOOK_PATH: str
    WEB_SERVER_HOST: str = "0.0.0.0"
    WEB_SERVER_PORT: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()