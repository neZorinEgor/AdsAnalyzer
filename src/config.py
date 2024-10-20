from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
    NGINX_HTTP_PORT: str
    NGINX_HTTPS_PORT: str

    APP_HOST: str
    APP_PORT: str

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

    @property   # for cache
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def jwt_private_key(self):
        BASE_PATH = Path(__file__).parent.parent
        private_key_path: Path = BASE_PATH / "src" / "user" / "keys" / "jwt-private.pem"
        return private_key_path.read_text()

    @property
    def jwt_public_key(self):
        BASE_PATH = Path(__file__).parent.parent
        private_key_path: Path = BASE_PATH / "src" / "user" / "keys" / "jwt-public.pem"
        return private_key_path.read_text()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
