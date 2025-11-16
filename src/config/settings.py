from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Storage
    data_dir: str = "data"

    # Application
    environment: str = "development"
    secret_key: str = "dev-secret-key-change-in-production"
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Car Rentar API"
    version: str = "0.1.0"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def data_path(self) -> Path:
        """Get the data directory path."""
        return Path(self.data_dir)


# Global settings instance
settings = Settings()
