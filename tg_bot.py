import logging
import os
import time

import telegram
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ContextTypes

from detect_intent import detect_intent_texts

logger = logging.getLogger("tg_bot_logger")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуй, {user.mention_html()}!",
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
    my_tg_chat_id = os.environ['TG_MY_CHAT_ID']

    tg_bot = telegram.Bot(token=bot_token)
    logging.basicConfig(filename='tg_bot_log.log', format="%(asctime)s - %(funcName)s(%(lineno)d): %(message)s")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, my_tg_chat_id))
    logger.warning('TG Бот запущен')

    while True:
        try:
            application = Application.builder().token(bot_token).build()

            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("help", help_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

            application.run_polling()

        except ConnectionError:
            logger.warning('Ошибка соединения')
            time.sleep(60)
            continue
        except Exception as exc:
            logger.warning(exc)
            continue


if __name__ == '__main__':
    main()
