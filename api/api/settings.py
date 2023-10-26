import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    domain: str = "localhost"
    host: str = "127.0.0.1"
    port: int = 8000
    web_uri: str = "http://localhost:3000/"
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "db"
    db_port: int = 5432
    db_user: str = "postgres_user"
    db_pass: str = "postgres_password"
    db_base: str = "app"
    db_echo: bool = False

    # github oauth
    github_client_id: str = ""
    github_client_secret: str = ""

    # token credentials
    token_algorithm: str = "HS512"
    token_secret_key: str = "app_some_secret_key"

    @property
    def is_production(self) -> bool:
        """
        This property checks if the environment is set to "production".

        :returns: True if the current environment is "production," False otherwise.
        """
        return self.environment == "production"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="API_",
        env_file_encoding="utf-8",
    )


settings = Settings()
