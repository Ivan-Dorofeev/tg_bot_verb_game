# Бот для VK и Telegram

## Описание

Боту общается по заранее подготовленным фразам, который храним в своём аккаунте [Dialogflow](https://dialogflow.cloud.google.com/)

**VK**  - [VK Group](https://vk.com/im?media=&sel=-194790108)

![vk_gif](https://user-images.githubusercontent.com/58893102/222070436-49f7884e-103a-4a0b-b5e5-e9c2a1b997dd.gif)


**Telegram** - [TG Bot](https://t.me/verb_game_bot)

![tg_gif](https://user-images.githubusercontent.com/58893102/222070418-aae63936-bbc3-42fa-ba86-584a3de23b0f.gif)


## Установка

- скачать репозиторий
- установите необходимы библиотеки командой:

    ```pip install -r requirements.txt```
    
- создайте файл ```.env``` в корневом каталоге
- положите в него:

    ```TG_BOT_TOKEN``` - токен от телеграмм бота

    ```TG_MY_CHAT_ID``` - свой айди чата
    
    ```VK_API_GROUP_TOKEN``` - токен VK группы
    
    ```DIALOGFLOW_PROJECT_ID``` - id своего проекта в [Dialogflow](https://dialogflow.cloud.google.com/)

## Развитие бота

Чтобы бот определял необходимые фразы и правильно отвечал, настройте это в [Dialogflow](https://dialogflow.cloud.google.com/):

- нажмите CREATE UNTENT
![image](https://user-images.githubusercontent.com/58893102/222640446-f944455d-95c2-4614-9f50-dc76a01d9386.png)

- пропишите фразы для отлова (Training phrases)

- пропишите ответ (Responses)

Получится примерно так:

![image](https://user-images.githubusercontent.com/58893102/222640855-9c57e7d4-f3ed-4ebb-ab66-1c98a0a61c57.png)


## Запуск

Запустите телеграмм-бота командой:

```python tg_bot.py```

Запустите VK-бота командой:

```python vk_bot.py```


## Логирование

О начале запуска и обо всех ошибках работы, бот информирует сообщением в телеграмм чат.
А также все логи телеграмм-бота пишет в ```tg_bot_log.log```, а логи от VK-бота в ```vk_bot_log.log```
