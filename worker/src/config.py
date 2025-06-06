from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # Broker
    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_ANALYSIS_TOPIC: str
    KAFKA_ANALYSIS_GROUP_ID: str
    # DirectAPI
    REPORT_SERVICE_URL: str
    # Database
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # Filestorage
    S3_HOST: str
    S3_PORT: str
    S3_BUCKET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    # LLM configuration
    # PATH_TO_LLM_PROMPT: Path
    # MAX_LLM_TOKENS: int
    YANDEX_CLOUD_FOLDER_ID: str
    YANDEX_CLOUD_IAM_TOKEN: str
    YANDEX_IAM_TOKEN_API_URL: str
    YANDEX_OAUTH_TOKEN: str

    PATH_TO_DIFFERENCE_PROMPT: Path = BASE_DIR / "prompts" / "difference_between_cluster_prompt.txt"
    PATH_TO_LLM_PROMPT: Path = BASE_DIR / "prompts" / "llm_role_prompt.txt"

    @property
    def kafka_url(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"

    @property
    def postgresql_utl(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def s3_endpoint_url(self):
        return f"http://{settings.S3_HOST}:{settings.S3_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # noqa
