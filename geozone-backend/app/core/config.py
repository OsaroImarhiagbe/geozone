import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment:str = os.getenv("ENVIRONMENT","development")
    api_v1_str: str = "/api/v1"
    project_name: str = "GeoZone"

    # Security settings
    secret_key: SecretStr

    # jwt access + refresh token
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    # Algorithm secret or not???
    algorithm:SecretStr

    # Redis
    redis_host:str
    redis_db:int
    redis_port:int
    redis_password:SecretStr

    #Postgres db
    postgresql_port:int
    alembic_postgres_user: str
    
    geozone_authenticated_postgres_user:str
    geozone_anon_postgres_user:str

    postgres_password: SecretStr
    postgres_db:str
    postgres_host:str

    ## Claude API Settings
    api_key: str
    model: str = "claude-sonnet-5-5"  # confirm against your provider's current model list
    max_tokens: int = 4000
    timeout_seconds: float = 60.0

    ordinance_version: str = "unset"
    prompt_version: str = "v1"

    # Hard cap on ordinance text sent per request (characters, ~4 chars/token)
    ordinance_char_budget: int = 24_000
    
    # CACHE_PREFIX = "geozone:analysis"
    # CACHE_TTL_SECONDS = 60 * 60 * 24  # move to settings; unviewed analyses expire

    # Alembic Database url -> Root User
    def alembic_database_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.alembic_postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgresql_port}/{self.postgres_db}"
    
    # FastAPI Database url -> Authenticated User
    def authenticated_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.geozone_authenticated_postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgresql_port}/{self.postgres_db}"

    # FastAPI Database url -> Anonymous User
    def anonymous_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.geozone_anon_postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgresql_port}/{self.postgres_db}"

    # Configuration for the model
    model_config = SettingsConfigDict(
        env_file=f".env.{environment}", 
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    


try:
    settings = Settings()
    print("Environment settings are available! ")
except Exception as e:
    print(f'Booting environment error:{e}')
    exit(1) # what does this do?
