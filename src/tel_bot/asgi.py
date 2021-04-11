from random import random, randint

import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

from tel_bot import telegram
from tel_bot.config import settings
from tel_bot.telegram.types import Update, SendMessage, setWebHook
from tel_bot.util import debug

TELEGRAM_BOT_API = f"https://api.telegram.org/bot{settings.bot_token}"
load_dotenv()

app = FastAPI()

async def getWebhookInfo():
    token = os.getenv("BOT_TOKEN")
    client_session = aiohttp.ClientSession(raise_for_status=True)
    resp = await client_session.post(f"https://api.telegram.org/bot{token}/getWebhookInfo", raise_for_status=False)
    text = await resp.json()
    url = text["result"]
    return url


@app.get("/")
async def index():
    data = await getWebhookInfo()
    url = data["url"]
    with open("src/index.html", "r", encoding='utf-8') as f:
        text = f.read()
    return HTMLResponse(text.format(value=url))


@app.post("/")
async def pas(request: Request):
    data = await request.body()
    pas_len=data.decode().split("=")
    password = pas_len[1]
    if password == os.getenv("PASSWORD"):
        token = os.getenv("BOT_TOKEN")
        telega_url=os.getenv("TELEGA_URL")
        reply = setWebHook(
            url="url",
            url_telega=f"{telega_url}webhook/",
        )
        client_session = aiohttp.ClientSession(raise_for_status=True)
        resp = await client_session.post(
            f"https://api.telegram.org/bot{token}/setWebHook",
            json=reply.dict(),
            raise_for_status=False
        )
        res = await resp.json()
        description = res["description"]
        value = f"{description} : {telega_url}webhook/"
        with open("index.html", "r", encoding='utf-8') as f:
            text = f.read()
    return HTMLResponse(text.format(value2=value))



@app.get("/settings/")
async def handle_settings():
    debug(settings)
    return settings


@app.post("/webhook/")
async def tg_webhook(update: Update):
    try:
        text ={
            1: "Привет",
            2:"Hello",
            3:"Здравейте",
            4:"Aloha",
            5:"Прывiтанне"
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

