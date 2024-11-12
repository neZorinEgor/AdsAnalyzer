from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Auth:
    public_jwt_key_path: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    auth: Auth = Auth()

    SMTP_EMAIL_FROM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_PASSWORD: str

    RABBITMQ_PORT: int
    RABBITMQ_HOST: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    @property
    def rabbitmq_url(self):
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
