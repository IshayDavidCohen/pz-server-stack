from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Storage
    DATA_DIR: str = "/data"

    # RCON / Status
    PZ_RCON_HOST: str = "10.0.0.18"
    PZ_RCON_PORT: int = 27015
    PZ_RCON_PASSWORD: str = ""
    PZ_STATUS_TTL_SECONDS: int = 2  # cache to avoid spamming RCON


settings = Settings()
