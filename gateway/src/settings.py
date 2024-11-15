from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    AUTH_SERVICE_URL: str
    NOTIFICATION_SERVICE_URL: str

    model_config = SettingsConfigDict(env_file=".env")
