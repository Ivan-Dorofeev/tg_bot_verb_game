import os
from dotenv import load_dotenv
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent import detect_intent_texts


def echo(event, vk_api):
    text = event.text
    project_id = 'axxel123-gtnf'
    session_id = event.user_id

    answer = detect_intent_texts(project_id, session_id, text, 'ru')
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_group_token = os.environ['VK_API_GROUP_TOKEN']
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
