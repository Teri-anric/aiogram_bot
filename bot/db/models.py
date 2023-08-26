from aiogram.enums.input_media_type import InputMediaType
from sqlalchemy import Column, Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from . import Base


class PostMedia(Base):
    __tablename__ = "post_media"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    post_id = Column(ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE"))
    type_media = Column(Enum(InputMediaType))
    tg_file_id = Column(Text)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(Text, nullable=True)
    media = relationship(PostMedia, uselist=True)
