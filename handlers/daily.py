from datetime import time as dtime, datetime, timedelta
from zoneinfo import ZoneInfo
from telegram.ext import CommandHandler, ContextTypes
import config

DEFAULT_TZ = ZoneInfo(getattr(config, "DEFAULT_TZ", "Europe/Minsk"))
DEFAULT_TIME = dtime(8, 0)


def _job_name(chat_id: int) -> str:
    return f"daily_weather_{chat_id}"


async def _job_ping(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        context.job.chat_id,
        "Утро доброе, солдат.\nУтренняя сводка от Денчика:"
    )


async def morning(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    t = DEFAULT_TIME
    if context.args:
        try:
            hh, mm = map(int, context.args[0].split(":"))
            t = dtime(hh, mm)
        except Exception:
            await update.message.reply_text("Формат: /morning HH:MM (например 07:30)")
            return

    aware_time = dtime(t.hour, t.minute, tzinfo=DEFAULT_TZ)

    jq = context.job_queue or context.application.job_queue
    if jq is None:
        await update.message.reply_text(
            'JobQueue недоступен. Установи: pip install "python-telegram-bot[job-queue]"'
        )
        return

    for j in jq.get_jobs_by_name(_job_name(chat_id)) or []:
        j.schedule_removal()

    jq.run_daily(
        _job_ping,
        time=aware_time,
        name=_job_name(chat_id),
        chat_id=chat_id,
    )

    now = datetime.now(DEFAULT_TZ)
    first_run = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    if first_run <= now:
        first_run += timedelta(days=1)

    await update.message.reply_text(
        f"Ок, шлём каждый день в {t:%H:%M} ({DEFAULT_TZ.key}). "
        f"Первый раз: {first_run:%Y-%m-%d %H:%M}."
        "\n/morning_off — выключить."
    )


async def morning_off(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jq = context.job_queue or context.application.job_queue
    if jq is None:
        await update.message.reply_text("JobQueue недоступен.")
        return
    jobs = jq.get_jobs_by_name(_job_name(chat_id)) or []
    if not jobs:
        await update.message.reply_text("У тебя нет активной утренней рассылки.")
        return
    for j in jobs:
        j.schedule_removal()
    await update.message.reply_text("Утренняя рассылка выключена.")


def register(app):
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("morning_off", morning_off))
