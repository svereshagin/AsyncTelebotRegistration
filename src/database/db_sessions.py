from src.database.database import Base, engine, connection
from src.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


@connection
async def get_users(telegram_id: str, session) -> int:
    """Вощвращает результат операции булевым значением
        необходимо передать параметр telegram_id"""
    try:
        # Выполняем запрос с фильтрацией по telegram_id
        res = await session.execute(
            select(User).filter(User.telegram_id == telegram_id)
        )
        users = res.scalars().all()  # Получаем список пользователей

        if not users:
            return 0  # Если пользователей нет, возвращаем 0
        else:
            return 1  # Если пользователи найдены, возвращаем 1
    except Exception as e:
        print(e)
        return -1  # Возвращаем -1 в случае ошибки


@connection
async def add_person(user, session: AsyncSession) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - user: User - объект пользователя, который нужно добавить в базу данных.
    - session: AsyncSession - асинхронная сессия базы данных.

    Возвращает:
    - int - идентификатор созданного пользователя.
    """
    try:
        # Добавляем пользователя в сессию
        session.add(user)  # Добавляем пользователя
        await session.commit()  # Коммитим изменения
        print(f"Added user: {user}")
        return user.id  # Возвращаем идентификатор пользователя
    except Exception as e:
        print(f"Error adding user: {e}")
        raise  # Поднимаем исключение дальше


async def reset_database():
    # Удаляем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Создаем все таблицы заново
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
