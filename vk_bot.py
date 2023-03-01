import logging
import os
import time

import telegram
from dotenv import load_dotenv
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent import detect_intent_texts

logger = logging.getLogger("vk_bot_logger")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def echo(event, vk_api, project_id):
    text = event.text
    session_id = event.user_id

    answer = detect_intent_texts(project_id, session_id, text, 'ru')
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    my_tg_chat_id = os.environ['TG_MY_CHAT_ID']
    vk_group_token = os.environ['VK_API_GROUP_TOKEN']
    dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']

    tg_bot = telegram.Bot(token=bot_token)
    logging.basicConfig(filename='tg_bot_log.log', format="%(asctime)s - %(funcName)s(%(lineno)d): %(message)s")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, my_tg_chat_id))
    logger.warning('VK Бот запущен')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api, dialog_flow_project_id)
        except ConnectionError:
            logger.warning('Ошибка соединения')
            time.sleep(60)
            continue
        except Exception as exc:
            logger.warning(exc)
            continue
