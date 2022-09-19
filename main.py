import os

from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    print(__version_info__)
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


def detect_intent_texts(project_id, session_id, texts, language_code):
    credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Сам ты Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_chat_id = os.environ['TG_MY_CHAT_ID']
    message = update.message.text
    print(message)

    detect_intent_texts(project_id='axxel123-gtnf', session_id=tg_chat_id, texts=message, language_code='ru-RU')
    await update.message.reply_text(update.message.text)


def main():
    load_dotenv()

    tg_token = os.environ['TG_BOT_TOKEN']

    application = ApplicationBuilder().token(tg_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == '__main__':
    main()
