from pydantic import BaseSettings, SecretStr, PostgresDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn
    chat_id: int
    admin_id: int

    class Config:
        env_file = r'C:\Users\2005a\source\python\aiogram_bot\.env'
        env_file_encoding = 'utf-8'


config = Settings()
