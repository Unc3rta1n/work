from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship
import configparser
from sqlalchemy.sql import func
import bcrypt


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime(timezone=True), server_default=func.now())

    def set_password(self, plaintext_password):
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')


class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    authorization_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sessions")


config = configparser.ConfigParser()  # создаём объект парсера
config.read("settings.ini")  # читаем конфиг

# Получаем данные из конфигурации
username = config["SQLAlchemy"]["username"].strip('"')
password = config["SQLAlchemy"]["password"].strip('"')
# убираем одни кавычки, иначе строка получается в двойных кавычках

# Создаем строку подключения с использованием f-строки
connection_string = f"postgresql://{username}:{password}@localhost/Cappa_bot"
engine = create_engine(connection_string)

# создаем таблицы
Base.metadata.create_all(bind=engine)
