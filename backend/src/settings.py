from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class _Auth:
    PRIVATE_JWT_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
    PUBLIC_JWT_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_DAYS: timedelta = timedelta(days=1)
    BAN_MESSAGE: str = "BANNED"


class Settings(BaseSettings):
    auth: _Auth = _Auth()

    APP_HOST: str
    APP_PORT: str
    INITIAL_ADMIN_EMAIL: str
    INITIAL_ADMIN_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str

    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_DATABASE: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str

    FLOWER_USERNAME: str
    FLOWER_PASSWORD: str
    FLOWER_PORT: str

    S3_HOST: str
    S3_BUCKETS: str
    GATEWAY_LISTEN: str
    SERVICES: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    NGINX_HTTP_PORT: str

    @property
    def mysql_async_url(self):
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property   # for black list and cache
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def s3_endpoint_url(self):
        return f"http://{settings.S3_HOST}:{settings.GATEWAY_LISTEN}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # noqa
