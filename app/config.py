from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    app_name: str = "Taller_vehicular"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
