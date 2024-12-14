import asyncio
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DB_CONFIG
# Определяем базовый класс для моделей
Base = declarative_base()

# Определяем модель
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
    echo=True,
)

# Создаем асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)

async def create_user(name: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(name=name)
            session.add(user)
        await session.commit()


async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT * FROM users")
        users = result.fetchall()
        return users


async def main():
    await init_db()  # Инициализация базы данных
    await create_user("Alice")  # Создание пользователя
    await create_user("Bob")  # Создание пользователя
    users = await get_users()  # Получение всех пользователей
    for user in users:
        print(user)
