from pydantic import BaseSettings

class Settings(BaseSettings):
bot_token: str
admin_group_id: int
database_url: str
faq_url: str
remind_interval: int = 3600

class Config:
    env_file = ".env"

settings = Settings()