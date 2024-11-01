from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Auth:
    private_jwt_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
    public_jwt_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 120


class Settings(BaseSettings):
    auth: Auth = Auth()
    # proxy
    NGINX_HTTP_PORT: str
    NGINX_HTTPS_PORT: str
    # application
    APP_HOST: str
    APP_PORT: str
    # cache
    REDIS_HOST: str
    REDIS_PORT: str
    # relation database
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_DATABASE: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str
    # S3 `object` storage
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str
    S3_PORT: str
    S3_HOST: str

    @property   # for migration
    def mysql_url(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property   # for application
    def mysql_async_url(self):
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property   # for cache
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def jwt_private_key(self):
        BASE_PATH = Path(__file__).parent.parent
        private_key_path: Path = BASE_PATH / "src" / "auth" / "certs" / "jwt-private.pem"
        return private_key_path.read_text()

    @property
    def jwt_public_key(self):
        BASE_PATH = Path(__file__).parent.parent
        private_key_path: Path = BASE_PATH / "src" / "auth" / "certs" / "jwt-public.pem"
        return private_key_path.read_text()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
