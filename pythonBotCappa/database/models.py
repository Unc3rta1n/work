from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from database.session import engine
from sqlalchemy.sql import func
import bcrypt


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime(timezone=True), server_default=func.now())
    sessions = relationship("Sessions", back_populates="user")

    def set_password(self, plaintext_password):
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')


class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    authorization_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sessions")


# Таблица для второго бота, будет хранить sender_id
# которые ему хотя бы раз написали /start и при каждом реге\логине будет кидать уведы всем
class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String, unique=True, nullable=False)


# создаем таблицы
Base.metadata.create_all(bind=engine)
