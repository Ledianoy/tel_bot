from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    debug: bool = Field(env="DEBUG", default=False)
    python_path: str = Field(..., env="PYTHONPATH")
    service_url: str = Field(..., env="SERVICE_URL")
    url: str = Field(default="url")
    url_telega: str = Field(..., env="TELEGA_URL")
    index_path: str = Field(..., env="INDEX_PATH")


    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

class Pass(BaseSettings):
    password: str

settings: Settings = Settings()