# Бота для VK и Telegram

## Описание

Боту общается по заранее подготовленным фразам, который храним в своём аккаунте [Dialogflow](https://dialogflow.cloud.google.com/)

VK 
[image](https://user-images.githubusercontent.com/58893102/222063889-91037c30-a6ec-46c1-a11a-4b544193f0c2.png)


Telegram
[image](https://user-images.githubusercontent.com/58893102/222063820-0d9faac8-665a-4cd4-966b-03625f8c6eb6.png)



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

## Запуск

Запустите телеграмм-бота командой:

```python tg_bot.py```

Запустите VK-бота командой:

```python vk_bot.py```


## Логирование

О начале запуска и обо всех ошибках работы, бот информирует сообщением в телеграмм чат.
А также все логи телеграмм-бота пишет в ```tg_bot_log.log```, а логи от VK-бота в ```vk_bot_log.log```
