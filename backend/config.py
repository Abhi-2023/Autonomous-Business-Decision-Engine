from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError
from functools import lru_cache

class Settings(BaseSettings):
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(1440, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field("HS256", env="ALGORITHM")

    database_url: str = Field(..., env="DATABASE_URL")

    redis_url: str = Field(..., env="REDIS_URL")

    qdrant_url: str = Field(..., env="QDRANT_URL")
    qdrant_collection: str = Field("documents", env="QDRANT_COLLECTION")

    llm_model: str = Field("claude-3-sonnet-20240229", env="LLM_MODEL")
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")

    log_level: str = Field("INFO", env="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
        

@lru_cache
def get_settings():
    return Settings()