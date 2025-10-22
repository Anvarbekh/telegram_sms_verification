from pydantic import BaseSettings, AnyHttpUrl
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    telegram_api_token: str
    database_url: str
    webhook_host: str | None = None
    callback_path: str = "/api/v1/webhook/report"
    service_port: int = 8000
    code_ttl_seconds: int = 60
    code_length: int = 6

    class Config:
        env_file = ".env"


settings = Settings()


