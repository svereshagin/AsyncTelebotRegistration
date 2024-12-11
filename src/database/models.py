# Импорты из библиотеки SQLAlchemy
from sqlalchemy import (
    MetaData, Table, Column, BIGINT, Integer, String, Text,
    DateTime, Boolean, ForeignKey, SmallInteger, func
)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, selectinload
from sqlalchemy.future import select

# Другие импорты
import asyncio
import datetime
from typing import List, Optional

# Конфигурация для подключения к базе данных
from ..config import DB_CONFIG

#
# class Base(AsyncAttrs, DeclarativeBase):
#     pass
#
# metadata = MetaData()
#
# class User(Base):
#     __tablename__ = 'users'
#
#     user_id = Column(BIGINT(), primary_key=True)
#     first_name = Column(Text())
#     last_name = Column(Text())
#     sex = Column(Integer())  # 0 - female, 1 - male
#     age = Column(Integer())
#     date_of_birth = Column(DateTime())
#     telegram_id = Column(BIGINT(), unique=True)
#     email = Column(Text())
#     city = Column(Text())
#     geolocation = Column(Text())
#     privileges = Column(Text())
#     status = Column(Integer())  # 0: inactive, 1: in search, 2: in game
#
#     # Relationships
#     in_game_user = relationship("InGameUser ", back_populates="user")
#     user_statistics = relationship("User Statistics", back_populates="user")
#     sessions = relationship("Session", back_populates="host")
#
# class InGameUser (Base):
#     __tablename__ = 'in_game_users'
#
#     user_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
#     user_health_points = Column(BIGINT())
#     user_exp = Column(BIGINT())
#     user_money_gold = Column(BIGINT())
#     user_money_silver = Column(BIGINT())
#     user_money_bronze = Column(BIGINT())
#     is_adult = Column(Boolean())
#
#     # Relationships
#     user = relationship("User ", back_populates="in_game_user")
#
# class UserStatistics(Base):
#     __tablename__ = 'user_statistics'
#
#     user_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
#     endgames = Column(Integer())
#     done_quests = Column(Integer())
#     declined_challenges = Column(Integer())
#     reports = Column(Integer())
#
#     # Relationships
#     user = relationship("User ", back_populates="user_statistics")
#
# class Session(Base):
#     __tablename__ = 'sessions'
#
#     host_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
#     players_quantity = Column(SmallInteger())
#     status = Column(Boolean())
#     password = Column(Integer())
#     is_adm = Column(Boolean())
#     players = Column(Text())
#     created_at = Column(DateTime())
#
#     # Relationships
#     host = relationship("User ", back_populates="sessions")
#
#
# async def async_main():
#     """Main program function."""
#
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     async_session = async_sessionmaker(engine, expire_on_commit=False)
#
#     async with async_session() as session:
#         async with session.begin():
#             # Добавление нескольких пользователей и их игровых данных
#             session.add_all(
#                 [
#                     User(
#                         first_name="John", last_name="Doe", sex=1, age=30,
#                         date_of_birth=datetime.datetime(1994, 1, 1), telegram_id=1234567890,
#                         email="john.doe@example.com", city="New York", geolocation="40.7128, -74.0060",
#                         privileges="admin", status=1,
#                         in_game_user=[InGameUser(user_health_points=100, user_exp=50, user_money_gold=1000, user_money_silver=500, user_money_bronze=300, is_adult=True)],
#                         user_statistics=[UserStatistics(endgames=10, done_quests=5, declined_challenges=2, reports=1)],
#                         sessions=[Session(players_quantity=5, status=True, password=1234, is_adm=True, players="John, Mike", created_at=datetime.datetime.now())]
#                     ),
#                     User(
#                         first_name="Jane", last_name="Smith", sex=0, age=25,
#                         date_of_birth=datetime.datetime(1999, 5, 21), telegram_id=9876543210,
#                         email="jane.smith@example.com", city="Los Angeles", geolocation="34.0522, -118.2437",
#                         privileges="user", status=2,
#                         in_game_user=[InGameUser(user_health_points=90, user_exp=40, user_money_gold=800, user_money_silver=600, user_money_bronze=200, is_adult=True)],
#                         user_statistics=[UserStatistics(endgames=5, done_quests=3, declined_challenges=1, reports=0)],
#                         sessions=[Session(players_quantity=3, status=False, password=5678, is_adm=False, players="Jane, Mike", created_at=datetime.datetime.now())]
#                     )
#                 ]
#             )
#
#         # Загрузка всех пользователей с их игровыми данными и статистикой
#         stmt = select(User).options(selectinload(User.in_game_user), selectinload(User.user_statistics), selectinload(User.sessions))
#
#         # Выполнение запроса и вывод результатов
#         result = await session.scalars(stmt)
#
#         # result - это объект типа BufferedResult
#         for user in result:
#             print(f"User: {user.first_name} {user.last_name}")
#             print(f"Created at: {user.date_of_birth}")
#             for in_game_user in user.in_game_user:
#                 print(f"In-Game Stats: Health={in_game_user.user_health_points}, EXP={in_game_user.user_exp}")
#             for user_stat in user.user_statistics:
#                 print(f"User Statistics: Endgames={user_stat.endgames}, Done Quests={user_stat.done_quests}")
#             for session in user.sessions:
#                 print(f"Session: {session.players_quantity} players, Status={session.status}")
#
#         # Для асинхронной выборки с потоковой передачей данных
#         result = await session.stream(stmt)
#
#         # Используем поток для асинхронной выборки
#         async for user in result.scalars():
#             print(f"Streaming User: {user.first_name} {user.last_name}")
#             for in_game_user in user.in_game_user:
#                 print(f"In-Game Stats (streaming): Health={in_game_user.user_health_points}, EXP={in_game_user.user_exp}")
#
#         # Пример изменения данных
#         stmt_update = select(User).order_by(User.user_id)
#
#         result = await session.scalars(stmt_update)
#         user_to_update = result.first()
#
#         # Изменение данных пользователя
#         if user_to_update:
#             user_to_update.first_name = "Updated Name"
#             await session.commit()
#
#         # Пример использования интерфейса AsyncAttrs для ленивой загрузки
#         for in_game_user in await user_to_update.awaitable_attrs.in_game_user:
#             print(f"Lazily loaded in-game stats: Health={in_game_user.user_health_points}")


engine = create_async_engine(
        f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
        echo=True,
    )