from datetime import datetime
from typing import Annotated, List
from sqlalchemy import ARRAY, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


from config import settings


DATABASE_URL = settings.DATABASE_SQLITE

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


uniq_str_an = Annotated[str, mapped_column(unique=True)]

array_or_none_an = Annotated[List[str] | None, mapped_column(ARRAY(String))]
content_an = Annotated[str | None, mapped_column(Text)]

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
