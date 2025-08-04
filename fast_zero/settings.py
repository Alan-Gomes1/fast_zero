from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str
    FAKE_PASSWORD: str
    ALGORITHM: str
    EXPIRE_MINUTES: int
    SECRET_KEY_JWT: str
