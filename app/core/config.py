from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DEBUG: bool = True
    DATABASE_URL: str
    PROJECT_NAME: str = "LeadPro AI"
    VERSION: str = "0.0.1"


settings = Settings()