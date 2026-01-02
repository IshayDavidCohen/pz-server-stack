from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    WORKER_BASE_URL: str = "http://control-worker:8001"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"

    # Server join info (for building steam join URL)
    PZ_LAN_HOST: str = "10.0.0.18"
    PZ_PUBLIC_HOST: str = ""          # e.g. DDNS hostname or public IP
    PZ_GAME_PORT: int = 16261
    PZ_SERVER_PASSWORD: str = ""      # if your server has a password
    LAN_CIDRS: str = "10.0.0.0/24"

settings = Settings()
