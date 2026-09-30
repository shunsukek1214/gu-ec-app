from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # DB
    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    #Google
    google_client_id: str

def get_settings() -> Settings:
    return Settings()

settings = get_settings()

