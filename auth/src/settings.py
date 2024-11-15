import datetime
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Auth:
    PRIVATE_JWT_KEY_PATH: Path = BASE_DIR / "core" / "certs" / "jwt-private.pem"
    PUBLIC_JWT_KEY_PATH: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: datetime.timedelta = datetime.timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_DAYS: datetime.timedelta = datetime.timedelta(days=7)
    BAN_MESSAGE: str = "BANNED"


class Settings(BaseSettings):
    auth: Auth = Auth()

    APP_HOST: str
    APP_PORT: str
    INITIAL_ADMIN_EMAIL: str
    INITIAL_ADMIN_PASSWORD: str

    SMTP_EMAIL_FROM: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str

    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_DATABASE: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str

    @property   # for migration
    def mysql_url(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property   # for application
    def mysql_async_url(self):
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property   # for black list and cache
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
