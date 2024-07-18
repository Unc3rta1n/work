import asyncio
from datetime import datetime

from telethon import TelegramClient, events, Button
import logging

from database.models import Notifications, User, Sessions
from utils.setting import *
from database.session import Sessionlocal
from sqlalchemy.sql import func

config = get_config()

api_id = int(config["Telethon"]["api_id2"])
api_hash = config["Telethon"]["api_hash2"]
# Создать клиент телеграм-бота
client = TelegramClient('123', int(config["Telethon"]["api_id2"]), config["Telethon"]["api_hash2"]).start(
    bot_token=config["Telethon"]["bot_token2"])

last_time_check = func.now()
inc = 0


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.text('/notify')],
        [Button.text('/do_not_notify')]
    ]
    await event.respond('Привет я Каппа_бот. Жми /notify и я буду уведомлять тебя о регистрациях/авторизациях '
                        'пользователей на cappa.csu.ru)?',
                        buttons=buttons)
    logging.info(f'Команда /start получена от {event.sender_id}')


@client.on(events.NewMessage(pattern='/notify'))
async def notify(event):
    try:
        with Sessionlocal() as db:
            notification = Notifications(sender_id=event.sender_id)
            db.add(notification)
            db.commit()
    except Exception as e:
        logging.error(f"Ошибка при подписке на уведомления :  {e}")


# Функция для отправки уведомлений всем подписчикам
async def send_notifications(message):
    try:
        with Sessionlocal() as db:
            subscribers = db.query(Notifications).all()
        for subscriber in subscribers:
            await client.send_message(int(subscriber.sender_id), message)
    except Exception as e:
        print(f'Failed to send message: {e}')


# Функция для проверки новых регистраций
async def check_new_registrations():
    global last_time_check
    try:
        with Sessionlocal() as db:
            new_users = db.query(User).filter(User.registration_time > last_time_check).all()
            for user in new_users:
                logging.info(f'найдены новые юзеры делаю рассылку ')
                await send_notifications(f'Новый пользователь зарегистрировался!: {user.username}')
            new_sessions = db.query(Sessions).filter(Sessions.authorization_time > last_time_check).all()
            for session in new_sessions:
                logging.info(f'найдены новые сессии делаю рассылку ')
                user = db.query(User).filter(session.user_id == User.id).first()
                await send_notifications(f'Старый пользователь авторизовался!: {user.username}')
            if not new_users or new_sessions:
                logging.info('ниче не найдено')
            else:
                logging.info('Отправлено уведомление')
    except Exception as e:
        print(f'Ошибка при обработке : {e}')

    # Обновляем время последней проверки
    last_time_check = datetime.now()


# Периодическая проверка базы данных
async def periodic_check():
    while True:
        await check_new_registrations()
        await asyncio.sleep(60)  # Проверять каждую минуту
