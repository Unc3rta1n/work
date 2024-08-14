from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    pk_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, unique=True)

    folders = relationship("Folder", back_populates="user")


class Folder(Base):
    __tablename__ = 'folders'

    pk_id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.pk_id'))

    user = relationship("User", back_populates="folders")
    files = relationship("File", back_populates="folder")


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    folder_id = Column(Integer, ForeignKey('folders.pk_id'))

    folder = relationship("Folder", back_populates="files")
    links = relationship("Link", back_populates="file")


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    file_id = Column(Integer, ForeignKey('files.id'))

    file = relationship("File", back_populates="links")
