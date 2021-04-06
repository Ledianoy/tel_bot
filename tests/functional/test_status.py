import os
import pytest
from starlette import status
from starlette.testclient import TestClient

from asgi import app
from dotenv import load_dotenv

client = TestClient(app)

load_dotenv()

PATH = os.getenv("PYTHONPATH")
TOKEN = os.getenv("BOT_TOKEN")


@pytest.mark.functional
def test_status_localhost():
    response = client.get("/config/")
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    data = {"bot_token": TOKEN, "pythonpath": PATH}
    assert payload == data


@pytest.mark.functional
def test_status_heroku():
    response = client.get("https://tel-bot-z43.herokuapp.com/config/")
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    data = {"bot_token": os.getenv('BOT_TOKEN'), "pythonpath": os.getenv('PYTHONPATH')}
    assert payload == data