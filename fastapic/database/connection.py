from contextlib import asynccontextmanager
from uuid import uuid4
from asyncpg import Connection
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from database.models import User, Base, Folder, File, Link
from utils.utils import get_config
import logging

config = get_config()


class DBConnection:
    def __init__(self):
        self.engine = None
        self.session = None

        try:
            db_user = config.get('SQLAlchemy', 'username')
            db_pass = config.get('SQLAlchemy', 'password')
            db_host = config.get('SQLAlchemy', 'db_host')
            db_port = config.get('SQLAlchemy', 'db_port')
            db_name = config.get('SQLAlchemy', 'db_name')

            self.engine = create_async_engine(
                f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
            self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

        except Exception as e:
            logging.error("Ошибка при инициализации подключения к PostgreSQL: %s", e)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def create_session(self):
        async with self.session() as db:
            try:
                yield db
            except Exception as e:
                await db.rollback()
                logging.error("Ошибка в сессии базы данных: %s", e)
                raise
            finally:
                await db.close()

    async def auth_user(self, user: str):
        async with self.create_session() as db:
            data = insert(User).values(tg_id=user)
            await db.execute(data)
            await db.commit()

    async def check_auth_user(self, user: str):
        async with self.create_session() as db:
            data = select(User).where(User.tg_id == user)
            result = (await db.execute(data)).all()
            return bool(result)

    async def check_folder(self, folder: str):
        async with self.create_session() as db:
            data = select(Folder).where(Folder.name == folder)
            result = (await db.execute(data)).all()
            return bool(result)

    async def create_folder(self, folder: str):
        async with self.create_session() as db:
            data = select(User).where(User.tg_id == folder)
            result = (await db.execute(data)).all()
            user_id = result.scalar_one_or_none()
            if not user_id:
                raise ValueError(f"В базе нет юзера с таким айди: {folder}")
            query = insert(Folder).values(name=folder, user_id=user_id)

            await db.execute(query)
            await db.execute(data)
            await db.commit()

    async def get_filename(self, link_url):
        async with self.create_session() as db:
            query = (
                select(File.name)
                .join(Link, File.id == Link.file_id)
                .where(Link.link == link_url)
            )
            result = (await db.execute(query)).first()
            return result[0]

    async def create_file(self, folder_name: str, file_name: str, link_url: str):
        async with self.create_session() as db:

            query = select(User).where(User.tg_id == folder_name)
            result = await db.execute(query)
            user = result.scalars().first()

            if user is None:
                user = User(tg_id=folder_name)
                db.add(user)
                await db.flush()

            query = select(Folder).where(Folder.name == folder_name, Folder.user_id == user.pk_id)
            result = await db.execute(query)
            folder = result.scalars().first()

            if folder is None:
                folder = Folder(name=folder_name, user_id=user.pk_id)
                db.add(folder)
                await db.flush()

            file = File(name=file_name, folder_id=folder.pk_id)
            db.add(file)
            await db.flush()

            link = Link(link=link_url, file_id=file.id)
            db.add(link)
            await db.commit()

    async def show_links(self, folder_name: str):
        async with self.create_session() as db:
            query = (
                select(Folder)
                .options(selectinload(Folder.files).selectinload(File.links))
                .where(Folder.name == folder_name)
            )
            result = await db.execute(query)
            folder = result.scalar_one_or_none()

            file_list = []
            if folder:
                for idx, file in enumerate(folder.files, start=1):
                    for link in file.links:
                        file_list.append(f"{idx}. {file.name}: http://agent:8080/file?f={link.link}")
            else:
                return f"В папке '{folder_name}' нет файлов."
            file_list_string = " \n".join(file_list)
            return file_list_string
