from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import config

from utils.weather import geocode_city, get_current_weather


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_city = config.get_city(context)
    await update.message.reply_text(user_city)
    try:
        lat, lon, norm_name, country = geocode_city(user_city)
        w = get_current_weather(norm_name)
        text = (
            f"Понял город как: {norm_name}, {country}\n"
            f"{w['weather']}\n"
            f"Температура: {w['temp_c']}°C\n"
            f"Ветер: {w['wind_m_s']} м/с\n"
            f"Влажность: {w.get('humidity') if w.get('humidity') is not None else '—'}%\n"
            f"Время измерения: {w['time']}"
        )
    except ValueError:
        text = (
            "Не понял город 🤔. Проверь написание города в /city\n"
            "Примеры:\n"
            "  Минск\n"
            "  Санкт-Петербург\n"
            "  Warsaw\n"
        )
    except Exception as e:
        text = f"Ошибка при получении погоды: {e}"

    await update.message.reply_text(text)
