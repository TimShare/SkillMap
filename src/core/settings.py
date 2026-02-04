from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    database_url: str = Field(...)
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="skillmap")
    db_user: str = Field(default="user")
    db_password: str = Field(default="password")
    
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    title: str = "SkillMap API"
    version: str = "1.0.0"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
