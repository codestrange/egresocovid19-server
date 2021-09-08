from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    access_token_algorithm: str = "HS256"
    access_token_secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_algorithm: str = "HS256"
    refresh_token_secret_key: str
    refresh_token_expire_minutes: int = 365 * 24 * 60

    class Config:
        env_file = ".env"


settings = Settings()


def get_settings():
    return settings
