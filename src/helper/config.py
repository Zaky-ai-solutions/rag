from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_MAX_SIZE: int # mega Bytes
    FILE_ALLOWED_TYPES: list
    FILE_DEFAULT_CHUNK_SIZE: int
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()