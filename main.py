import os
from telegram.ext import Application, CommandHandler
from handlers.start import start as start_handler
from handlers.weather import weather
from handlers.city import register as city_register
from handlers.daily import register as daily_register
from config import TOKEN


def build_app():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("weather", weather))
    city_register(app)
    daily_register(app)
    return app


def main():
    app = build_app()

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
