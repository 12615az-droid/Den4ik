import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_CITY = "Минск"


def get_city(context):
    return context.bot_data.get("city", DEFAULT_CITY)


def set_city(context, city: str):
    context.bot_data["city"] = city
