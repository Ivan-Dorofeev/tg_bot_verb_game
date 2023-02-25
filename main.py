import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ContextTypes

from detect_intent import detect_intent_texts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуй, {user.mention_html()}!",
        # reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Сам себе Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texts = update.message.text
    project_id = 'axxel123-gtnf'
    session_id = update.message.id
    answer = detect_intent_texts(project_id, session_id, texts, 'ru')
    await update.message.reply_text(answer)


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    axxel123_GTNF_API_KEY = os.environ['axxel123_GTNF_API_KEY']

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()
