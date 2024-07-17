import logging
import configparser
import bcrypt
from telethon import TelegramClient, events
from createdb import User, Sessions
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[console_handler])

config = configparser.ConfigParser()  # создаём объект парсера
config.read("settings.ini")  # читаем конфиг

# Получаем данные из конфигурации
username = config["SQLAlchemy"]["username"]
password = config["SQLAlchemy"]["password"]
db_name = config["SQLAlchemy"]["db_name"]

# Создаем строку подключения с использованием f-строки
connection_string = f"postgresql://{username}:{password}@localhost/{db_name}"

# Запускаем движок и создаем сессию
engine = create_engine(connection_string, echo=False)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создать клиент телеграм-бота
client = TelegramClient('bot', int(config["Telethon"]["api_id"]), config["Telethon"]["api_hash"]).start(
    bot_token=config["Telethon"]["bot_token"])


# Обработчик для команды /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Привет я Каппа_бот. Ты хочешь зарегистрироваться(/registrate) или зайти в аккаунт('
                        '/authorization)?')
    logging.info(f'Команда /start получена от {event.sender_id}')


# Обработчик для команды /registrate
@client.on(events.NewMessage(pattern='/registrate'))
async def registrate(event):
    async with client.conversation(event.sender_id) as conv:
        while True:
            await conv.send_message('Введите ваш логин:')
            logging.info(f'Команда /registrate получена от {event.sender_id}')
            login = await conv.get_response()
            try:
                with Sessionlocal() as db:
                    user_data = db.query(User).filter_by(username=login.text).first()
                    if user_data:
                        await conv.send_message('Этот логин уже существует. Попробуйте другой.')
                        logging.info(f'Попытка регистрации с уже существующим логином: {login.text}')
                    else:
                        await conv.send_message('Введите ваш пароль:')
                        user_password = await conv.get_response()

                        new_user = User(username=login.text)
                        new_user.set_password(user_password.text)
                        db.add(new_user)
                        db.commit()
                        await conv.send_message('Вы успешно зарегистрированы!')
                        logging.info(f'Пользователь {login.text} успешно зарегистрирован.')
                        break
            except Exception as e:
                logging.error(f"Ошибка при регистрации пользователя в базу данных: {login.text}: {e}")
                await conv.send_message('Произошла ошибка при попытке записи в базу данных.')


# Функция, возвращающая список зарегистрированных пользователей
def get_all_usernames() -> list:
    try:
        with Sessionlocal() as db:
            users = db.query(User.username).all()
            usernames = [user.username for user in users]
            return usernames
    except Exception as e:
        logging.error(f"Ошибка при выборке имен пользователей: {e}")
        return []


# Функция, возвращающая хешированный пароль
def get_hashed_password(login: str) -> str | None:
    try:
        with Sessionlocal() as session:
            user = session.query(User).filter_by(username=login).first()
            if user:
                return user.password
            else:
                return None
    except Exception as e:
        logging.error(f"Ошибка при поиске хеш-пароля по логину {login}: {e}")
        return None


# Обработчик для команды /authorization
@client.on(events.NewMessage(pattern="/authorization"))
async def authorization(event):
    logging.info(f'Authorization command received from {event.sender_id}')
    usernames = get_all_usernames()
    if usernames:
        message = "Список пользователей:\n" + "\n".join(usernames)
    else:
        message = "Пользователи не найдены."

    logging.info(f'Возвращен список зарегистрированных пользователей {event.sender_id}')
    await client.send_message(event.sender_id, message)

    async with client.conversation(event.sender_id) as conv:

        message = "Выберите логин:"
        # тут кнопочками в чате хочется логины доступные сделать...
        await conv.send_message(message)
        while True:
            login = await conv.get_response()
            if login.text not in usernames:
                await conv.send_message('Неверный логин. Попробуйте другой.')
                logging.info(f'Попытка авторизации с незарегистрированным логином: {login.text}')
            else:
                hashed_password = get_hashed_password(login.text)
                if hashed_password:
                    while True:
                        await conv.send_message(f'Введите пароль от пользователя: {login.text}')
                        user_password = await conv.get_response()
                        hashed_user_password = bcrypt.hashpw(user_password.text.encode('utf-8'), bcrypt.gensalt())
                        hashed_user_password = hashed_user_password.decode('utf-8')
                        if bcrypt.checkpw(user_password.text.encode('utf-8'), hashed_password.encode('utf-8')):
                            break
                        else:
                            await conv.send_message(f'Неверный пароль от пользователя {login.text}')
                    try:
                        await conv.send_message(f'Пароли совпали, делаю авторизацию пользователя {login.text}')
                        with Sessionlocal() as db:
                            user = db.query(User).filter_by(username=login.text).first()
                            if user:
                                new_sess = Sessions(user_id=user.id)
                                db.add(new_sess)
                                db.commit()
                                await conv.send_message('Допустим зашли в аккаунт, отметили в базе данных')
                                break
                            else:
                                await conv.send_message('Пользователь не найден в базе данных.')
                    except Exception as e:
                        logging.error(f"Ошибка вставка сессии в бд для логина: {login.text}: {e}")
                        await conv.send_message('Произошла ошибка при попытке записи в базу данных.')

                else:
                    await conv.send_message('Пароль от пользователя не найден в базе данных .')


# Start the client
client.start()
client.run_until_disconnected()
