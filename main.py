import os
from telegram.ext import Application, CommandHandler
from handlers.start import start as start_handler
from handlers.weather import weather
from handlers.city import register as city_register
from handlers.daily import register as daily_register
from config import TOKEN


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("weather", weather))
    city_register(app)
    daily_register(app)
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        url_path=TOKEN,
        webhook_url=f"https://crooked-starlene-popovbot-21e32d60.koyeb.app/{TOKEN}",
    )


if __name__ == "__main__":
    main()
