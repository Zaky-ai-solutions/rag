from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_MAX_SIZE: int # mega Bytes
    FILE_ALLOWED_TYPES: list
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()