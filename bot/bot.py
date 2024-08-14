import os

from telethon import TelegramClient, events, Button
import httpx
from utils.utils import get_config
from utils.log import setup_logger

config = get_config()
logger = setup_logger('aboba', "DEBUG")

api_id = int(config["Telethon"]["api_id"])
api_hash = config["Telethon"]["api_hash"]
bot_token = config["Telethon"]["bot_token"]
client = TelegramClient('321', api_id, api_hash).start(
    bot_token=bot_token)

whitelist = [439810773, 5938529299, 694116221, 383803969, 157895821, 5573002896, 692115870, 613088017]


# Обработчик для команды /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if user_id in whitelist:
        await event.reply("Привет! Вы есть в белом списке.")
        api_url = f'http://fastapi_container:8000/create-folder/{event.sender_id}'
        #api_url = f'http://127.0.0.1:8001/create-user/{event.sender_id}'

        try:
            # запрос к фастапи на добавление юзера в бд
            async with httpx.AsyncClient() as aclient:
                response = await aclient.post(api_url)
            if response.status_code == 200:
                logger.info(f"Юзер '{event.sender_id}' успешно добавлен!")
            elif response.status_code == 409:
                logger.info(f"Юзер {event.sender_id} уже зарегистрирован")
            else:
                logger.error(f"Ошибка: {response.text}")
        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")

        await main_menu(event)


async def main_menu(event):
    keyboard = [
        [Button.inline("Получить ссылки", b'button1'), Button.inline("Загрузить файл", b'button2')],
        [Button.inline("Вернуться в главное меню", b'main_menu')]
    ]
    await event.respond("Выберите опцию:", buttons=keyboard)


@client.on(events.CallbackQuery())
async def callback(event):
    if event.data == b'button1':
        await show_links(event)
    elif event.data == b'button2':
        await upload_file(event)
    elif event.data == b'main_menu':

        await main_menu(event)


async def upload_file(event):
    async with client.conversation(event.sender_id) as conv:
        await conv.send_message("Пожалуйста, загрузите файл:")
        while True:
            response = await conv.get_response()
            if response.file:
                file = await response.download_media()
                await conv.send_message("Файл загружен на локальное хранилище успешно, отправляю на сервер...!")
                async with httpx.AsyncClient() as aclient:
                    with open(file, 'rb') as f:
                        files = {'file': (file, f)}
                        response = await aclient.post(
                            f'http://fastapi_container/create-file/{event.sender_id}', files=files)
                        data = response.json()
                        await conv.send_message(f"Файл загружен успешно и сохранен на сервере: {data['response_text']}")
                        os.remove(file)
                        break
            else:
                await conv.send_message("Пожалуйста, загрузите файл:")


async def show_links(event):
    async with httpx.AsyncClient() as aclient:
        response = await aclient.get(
            f'http://fastapi_container/show-links/{event.sender_id}')
        data = response.json()
        await event.respond(data)


# Запуск бота
client.start()
client.run_until_disconnected()
