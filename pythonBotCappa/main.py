import logging
import configparser
import bcrypt
import re
from telethon import TelegramClient, events, Button
from createdb import User, Sessions
from cappa_selenium import CappaAuth, CappaReg
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[console_handler])

config = configparser.ConfigParser()  # создаём объект парсера
config.read("settings.ini")  # читаем конфиг

# Получаем данные из конфигурационного файла
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

# Словарь для отслеживания состояния пользователей
user_states = {}


# Обработчик для команды /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.text('/registrate')],
        [Button.text('/authorizate')]
    ]
    await event.respond('Привет я Каппа_бот. Ты хочешь зарегистрироваться(/registrate) или зайти в аккаунт(/authorizate)?',
                        buttons=buttons)
    logging.info(f'Команда /start получена от {event.sender_id}')


# Функция, проверяющая валидность введенной почты
def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Обработчик для команды /registrate
@client.on(events.NewMessage(pattern='/registrate'))
async def registrate(event):
    user_id = event.sender_id
    if user_states.get(user_id) not in [None, '']:
        await event.respond("Вы уже выполняете другую команду. Завершите её перед началом новой.")
        return
    user_states[user_id] = 'registering'

    logging.info(f'Команда /registrate получена от {event.sender_id}')

    async with client.conversation(event.sender_id) as conv:
        while True:
            while True:
                await conv.send_message('Введите ваш логин:')
                logging.info(f'Команда /registrate получена от {event.sender_id}')
                login = await conv.get_response()
                if '/' in login.text:
                    await conv.send_message(
                        'Логин не должен содержать символ "/". Пожалуйста, попробуйте другой логин.')
                else:
                    break

            try:
                with Sessionlocal() as db:
                    user_data = db.query(User).filter_by(username=login.text).first()
                    if user_data:
                        await conv.send_message('Этот логин уже существует. Попробуйте другой.')
                        logging.info(f'Попытка регистрации с уже существующим логином: {login.text}')
                    else:
                        while True:
                            await conv.send_message('Введите  почту:')
                            email = await conv.get_response()
                            if is_valid_email(email.text):
                                break
                            else:
                                await conv.send_message('Ошибка в почте!')

                        await conv.send_message('Введите имя:')

                        f_name = await conv.get_response()  # тут пофиг на имя, никаких проверок на сайте нет
                        await conv.send_message('Введите фамилию:')

                        l_name = await conv.get_response()  # тут пофиг на фамилию, никаких проверок на сайте нет
                        while True:
                            await conv.send_message('Введите ваш пароль(больше 5 символов):')
                            user_password = await conv.get_response()  # тут пароль должен быть больше 5 символов
                            if len(user_password.text) <= 5:
                                await conv.send_message('Слабый пароль!')
                            else:
                                break

                        cappa = CappaReg(login.text, user_password.text, email.text, f_name.text, l_name.text)
                        value = cappa.registrate()

                        if value:
                            await conv.send_message(value)
                            raise Exception(value)

                        new_user = User(username=login.text)
                        new_user.set_password(user_password.text)
                        db.add(new_user)
                        db.commit()

                        await conv.send_message('Вы успешно зарегистрированы!')
                        logging.info(f'Пользователь {login.text} успешно зарегистрирован.')
                        break

            except Exception as e:
                logging.error(f"Ошибка при регистрации пользователя : {login.text}: {e}")
                user_states[user_id] = ''
                return
                # await conv.send_message('Произошла ошибка при попытке записи в базу данных.')


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


# Обработчик для команды /authorizate
@client.on(events.NewMessage(pattern="/authorizate"))
async def authorization(event):
    user_id = event.sender_id
    if user_states.get(user_id) not in [None, '']:
        await event.respond("Вы уже выполняете другую команду. Завершите её перед началом новой.")
        return
    user_states[user_id] = 'authorizing'

    logging.info(f'Команда /authorizate получена от {event.sender_id}')
    # await event.respond("Text", buttons=Button.clear()) волшебная вещь для удаления кнопок reply_keyboard
    try:
        async with client.conversation(event.sender_id) as conv:
            usernames = get_all_usernames()
            if usernames:
                # buttons = [[Button.inline(user_name, data=user_name)] for user_name in usernames]
                message = "Список пользователей:\n" + "\n".join(usernames)
                await event.respond(message)
            else:
                await event.respond("Пользователи не найдены.")
                return
            while True:
                while True:
                    await conv.send_message('Введите логин:')
                    login = await conv.get_response()
                    if '/' in login.text:
                        await conv.send_message(
                            'Логин не должен содержать символ "/". Пожалуйста, попробуйте другой логин.')
                    else:
                        break
                if login.text not in usernames:
                    await conv.send_message('Неверный логин. Попробуйте другой.')
                    logging.info(f'Попытка авторизации с незарегистрированным логином: {login.text}')
                else:
                    hashed_password = get_hashed_password(login.text)
                    if hashed_password:
                        while True:
                            await conv.send_message(f'Введите пароль от пользователя: {login.text}')
                            user_password = await conv.get_response()
                            if bcrypt.checkpw(user_password.text.encode('utf-8'), hashed_password.encode('utf-8')):
                                try:
                                    await conv.send_message(f'Пароли совпали, делаю авторизацию пользователя {login.text}')
                                    cappa = CappaAuth(login.text, user_password.text)
                                    value = cappa.authorizate()
                                    if value:
                                        await conv.send_message(value)
                                        raise Exception(value)

                                    with Sessionlocal() as db:
                                        user = db.query(User).filter_by(username=login.text).first()
                                        if user:
                                            new_sess = Sessions(user_id=user.id)
                                            db.add(new_sess)
                                            db.commit()
                                            await conv.send_message('Авторизация прошла успешно!')
                                            break
                                        else:
                                            await conv.send_message('Пользователь не найден в базе данных.')
                                except Exception as e:
                                    logging.error(f"Ошибка при авторизации пользователя: {login.text}: {e}")
                                    user_states[user_id] = ''
                                    return
                            else:
                                await conv.send_message(f'Неверный пароль от пользователя {login.text}')
                    else:
                        await conv.send_message('Пароль от пользователя не найден в базе данных.')
    except Exception as e:
        logging.error(f"Ошибка при авторизации пользователя: {login.text}: {e}")
        user_states[user_id] = ''
        return

    user_states[user_id] = ''

# Start the client
client.start()
client.run_until_disconnected()
