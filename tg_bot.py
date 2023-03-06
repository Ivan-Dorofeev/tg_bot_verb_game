import logging
import os
import time
from functools import partial
import telegram
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ContextTypes
from logging.handlers import RotatingFileHandler
from detect_intent import detect_intent_texts
from tg_log_sender import TelegramLogsHandler

logger = logging.getLogger("tg_bot_logger")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуй, {user.mention_html()}!",
    )


async def get_text_and_send_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, dialog_flow_project_id) -> None:
    texts = update.message.text
    session_id = update.message.id
    answer = detect_intent_texts(project_id=dialog_flow_project_id, session_id=session_id, text=texts,
                                 language_code='ru')
    await update.message.reply_text(answer)


def run_bot(bot_token, my_tg_chat_id, dialog_flow_project_id):
    tg_bot = telegram.Bot(token=bot_token)
    logging.basicConfig(filename='tg_bot_log.log', format="%(asctime)s - %(funcName)s(%(lineno)d): %(message)s")
    logger.setLevel(logging.INFO)

    tg_log_sender = TelegramLogsHandler(tg_bot, my_tg_chat_id)
    logger.addHandler(tg_log_sender)

    handler = RotatingFileHandler('tg_bot_log.log', maxBytes=5000000, backupCount=0)
    logger.addHandler(handler)

    logger.warning('TG Бот запущен')

    while True:
        try:
            application = Application.builder().token(bot_token).build()

            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                   partial(get_text_and_send_answer, dialog_flow_project_id=dialog_flow_project_id)))

            application.run_polling()

        except Exception as exc:
            logger.warning(exc)
            continue


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    my_tg_chat_id = os.environ['TG_MY_CHAT_ID']
    dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']

    run_bot(bot_token, my_tg_chat_id, dialog_flow_project_id)


if __name__ == '__main__':
    main()
