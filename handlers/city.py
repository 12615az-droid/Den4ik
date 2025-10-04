from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, \
    filters

import config

ASK_CONFIRM, TYPE_CITY = range(2)


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.get("city", config.DEFAULT_CITY)
    await update.message.reply_text(f"Текущий город: {current}")
    kb = [[
        InlineKeyboardButton("Да", callback_data="CITY_YES"),
        InlineKeyboardButton("Нет", callback_data="CITY_NO"),
    ]]

    await update.message.reply_text(
        f"Текущий город: {current}\nХотите поменять?",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return ASK_CONFIRM


async def city_yes_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "CITY_NO":
        await q.edit_message_text("Ок, ничего не меняем ✅")
        return ConversationHandler.END

    if q.data == "CITY_YES":
        await q.edit_message_text("Выбрано: поменять.")
        return TYPE_CITY

    await q.edit_message_text("Не понял кнопку. Попробуй ещё раз: /city")
    return ConversationHandler.END


async def city_set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_city = (update.message.text or "").strip()
    await update.message.reply_text(f"Вы выбрали: {new_city}")
    config.set_city(context, new_city)
    return ConversationHandler.END


async def city_invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Я жду название города *текстом*.\n"
        "Например: Москва\n"
        "Чтобы выйти — /cancel",
        parse_mode="Markdown"
    )
    return TYPE_CITY


async def city_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отмена. Ничего не меняю.")
    return ConversationHandler.END


def register(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler("city", city)],
        states={
            ASK_CONFIRM: [
                CallbackQueryHandler(city_yes_no, pattern="^CITY_(YES|NO)$"),
                CommandHandler("cancel", city_cancel),
            ],
            TYPE_CITY: [
                CommandHandler("cancel", city_cancel),
                MessageHandler(filters.TEXT & ~filters.COMMAND, city_set_text),
                MessageHandler(~filters.TEXT, city_invalid_input),
                MessageHandler(filters.COMMAND, city_invalid_input),
            ],
        },
        fallbacks=[],
    )
    app.add_handler(conv)
