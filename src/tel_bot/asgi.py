from random import randint

import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from starlette.templating import Jinja2Templates

from tel_bot.config import settings
from tel_bot.telegram.types import Update, SendMessage
from tel_bot.util import debug


TELEGRAM_BOT_API = f"https://api.telegram.org/bot{settings.bot_token}"
load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory=settings.index_path)

async def getWebhookInfo():
    token = os.getenv("BOT_TOKEN")
    client_session = aiohttp.ClientSession(raise_for_status=True)
    resp = await client_session.post(f"https://api.telegram.org/bot{token}/getWebhookInfo", raise_for_status=False)
    text = await resp.json()
    url = text["result"]
    return url


@app.get("/", response_class=HTMLResponse)
async def index(request: Request,):
    data = await getWebhookInfo()
    url = data["url"]
    context = {"value" : url}
    response = templates.TemplateResponse(
        "index.html", {"request": request, **context}
    )

    return response


@app.post("/", response_class=HTMLResponse)
async def pas(request: Request,):
    data = await request.body()
    pas_len=data.decode().split("=")
    password = pas_len[1]
    if password == os.getenv("PASSWORD"):
        telega_url=os.getenv("TELEGA_URL")
        url_telega=f"{telega_url}webhook/"
        client_session = aiohttp.ClientSession()
        resp = await client_session.post(
            f"{TELEGRAM_BOT_API}/setWebHook",
            json={"url": url_telega}
        )
        res = await resp.json()
        description = res["description"]
        value = f"{description} : {telega_url}webhook/"
        context = {"value2": value}
        response = templates.TemplateResponse(
            "index.html", {"request": request, **context}
        )

        return response


@app.get("/settings/")
async def handle_settings():
    debug(settings)
    return settings


@app.post("/webhook/")
async def tg_webhook(update: Update):
    try:
        text ={
            1: "????????????",
            2:"Hello",
            3:"??????????????????",
            4:"Aloha",
            5:"????????i??????????"
        }
        x= randint(1, 5)
        reply = SendMessage(
            chat_id=update.message.chat.id,
            text=text[x],
        )
        url = f"{TELEGRAM_BOT_API}/SendMessage"
        async with aiohttp.ClientSession() as session:
             async with session.post(url, json=reply.dict()) as response:
                payload = await response
                debug(response)
    finally:
        return {"ok": True}

