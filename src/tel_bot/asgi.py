
from dotenv import load_dotenv
from fastapi import FastAPI

from tel_bot.config import settings
from tel_bot.util import debug

load_dotenv()

app = FastAPI()


@app.get("/settings/")
async def handle_settings():
    debug(settings)
    return settings






