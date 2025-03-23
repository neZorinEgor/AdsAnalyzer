from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Broker
    KAFKA_HOST: str
    KAFKA_PORT: int
    ANALYSIS_TOPIC: str
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
