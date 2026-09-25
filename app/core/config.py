from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DEBUG: bool = True
    DATABASE_URL: str
    PROJECT_NAME: str = "LeadPro AI"
    VERSION: str = "0.0.1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    REFRESH_TOKEN_ROTATE_WINDOW_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    

settings = Settings()