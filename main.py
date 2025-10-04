
from telegram.ext import Application, CommandHandler

from config import TOKEN
from handlers import start, city, weather, daily
from handlers.city import register


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    register(application)
    daily.register(application)
    application.run_polling()


if __name__ == "__main__":
    main()
