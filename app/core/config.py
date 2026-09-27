
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+psycopg2://arun:arun@localhost:5432/leadpro"
    PROJECT_NAME: str = "LeadPro AI"
    VERSION: str = "0.0.1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    REFRESH_TOKEN_ROTATE_WINDOW_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = "heyarunyadav@gmail.com"
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "heyarunyadav@gmail.com"
    

settings = Settings()
