import logging
import configparser
from telethon import TelegramClient, events
from createdb import User, Sessions
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

# Получаем данные из конфигурации
username = config["SQLAlchemy"]["username"].strip('"')
password = config["SQLAlchemy"]["password"].strip('"')
# убираем одни кавычки, иначе строка получается в двойных кавычках

# Создаем строку подключения с использованием f-строки
connection_string = f"postgresql://{username}:{password}@localhost/Cappa_bot"
engine = create_engine(connection_string)
# Create the client and connect
client = TelegramClient('bot', int(config["Telethon"]["api_id"]), config["Telethon"]["api_hash"]).start(
    bot_token=config["Telethon"]["bot_token"])


# Handler for the /start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! I am a Cappa_bot. How can I assist you today?')
    logging.info(f'Start command received from {event.sender_id}')


@client.on(events.NewMessage(pattern='/registrate'))
async def registrate(event):
    async with client.conversation(event.sender_id) as conv:
        while True:
            await conv.send_message('Введите ваш логин:')
            logging.info(f'Registrate command received from {event.sender_id}')
            login = await conv.get_response()

            with Session(autoflush=False, bind=engine) as db:
                user_data = db.query(User).filter_by(username=login.text).first()
                if user_data:
                    await conv.send_message('Этот логин уже существует. Попробуйте другой.')
                    logging.info(f'Attempted registration with existing username: {login.text}')
                else:
                    await conv.send_message('Введите ваш пароль:')
                    user_password = await conv.get_response()

                    new_user = User(username=login.text)
                    new_user.set_password(user_password.text)
                    db.add(new_user)
                    db.commit()
                    await conv.send_message('Вы успешно зарегистрированы!')
                    logging.info(f'User {login.text} registered successfully.')
                    break

# Start the client
client.start()
client.run_until_disconnected()
