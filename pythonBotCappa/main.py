import logging
import configparser
from telethon import TelegramClient, events
from createdb import User, Sessions
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column
import bcrypt

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


# Handler for the /registrate command
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


# Function for getting registered names
def get_all_usernames() -> list:
    try:
        with Session(autoflush=False, bind=engine) as db:
            users = db.query(User.username).all()
            usernames = [user.username for user in users]
            return usernames
    except Exception as e:
        logging.error(f"Error fetching usernames: {e}")
        return []


# Function for getting hashed password
def get_hashed_password(login) -> str | None:
    try:
        with Session(autoflush=False, bind=engine) as session:
            user = session.query(User).filter_by(username=login).first()
            if user:
                return user.password
            else:
                return None
    except Exception as e:
        logging.error(f"Error fetching password for username {login}: {e}")
        return None


# Handler for the /authorization command
@client.on(events.NewMessage(pattern="/authorization"))
async def authorization(event):
    logging.info(f'Authorization command received from {event.sender_id}')
    usernames = get_all_usernames()
    if usernames:
        message = "Список пользователей:\n" + "\n".join(usernames)
    else:
        message = "Пользователи не найдены."

    logging.info(f'Returned list of registrated users {event.sender_id}')
    await client.send_message(event.sender_id, message)

    async with client.conversation(event.sender_id) as conv:
        message = "Выберите логин:"
        await conv.send_message(message)
        login = await conv.get_response()
        if login.text not in usernames:
            await conv.send_message('Неверный логин. Попробуйте другой.')
            logging.info(f'Attempted authorization with not existing username: {login.text}')
        else:
            hashed_password = get_hashed_password(login.text)
            if hashed_password:
                await conv.send_message(f'Захешированный пароль для пользователя {login.text}: {hashed_password}')

                try:
                    with Session(autoflush=False, bind=engine) as db:
                        user = db.query(User).filter_by(username=login.text).first()
                        if user:
                            new_sess = Sessions(user_id=user.id)
                            db.add(new_sess)
                            db.commit()
                            await conv.send_message('Допустим зашли в аккаунт, отметили в базе данных')
                        else:
                            await conv.send_message('Пользователь не найден в базе данных.')
                except Exception as e:
                    logging.error(f"Error inserting session for username {login.text}: {e}")
                    await conv.send_message('Произошла ошибка при попытке записи в базу данных.')

            else:
                await conv.send_message('Пользователь не найден.')

# Start the client
client.start()
client.run_until_disconnected()
