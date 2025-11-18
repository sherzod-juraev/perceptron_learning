from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_minutes: int
    refresh_token_days: int

    class Config:

        env_file = '.env'
        env_file_encoding = 'utf-8'