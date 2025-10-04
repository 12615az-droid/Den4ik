from telegram import Update
from telegram.ext import ContextTypes

from handlers.daily import morning


def _help_text():
    return (
        "Доступные команды:\n"
        "• /city — показать/сменить город\n"
        "• /weather — погода по сохранённому городу или по указанному аргументом\n"
        "• /morning [HH:MM] — включить утреннюю сводку (по умолчанию 08:00)\n"
        "• /morning_off — выключить утреннюю сводку\n"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Воин! Денчик на связи 🫡")
    await update.message.reply_text(_help_text())
    await morning(update, context)  # включит на DEFAULT_TIME
    await update.message.reply_text("Утренняя сводка подключена.")
