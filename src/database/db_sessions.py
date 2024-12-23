from sqlalchemy.orm.sync import update

from src.database.database import Base, engine, connection
from src.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

@connection
async def update_param(telegram_id: int, param: str, value, session: AsyncSession):
    """
    Обновление значения параметра по `telegram_id` в таблице User.

    Args:
        telegram_id (int): Telegram ID пользователя.
        param (str): Название параметра, которое нужно обновить.
        value: Новое значение параметра.
        session (AsyncSession): Сессия для работы с базой данных.

    Returns:
        bool: True, если обновление прошло успешно, False в случае ошибки.
    """
    try:
        # Проверить, существует ли параметр в модели User
        if not hasattr(User, param):
            raise ValueError(f"Параметр '{param}' не найден в модели User.")

        # Выполнить запрос на обновление
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values({param: value})
        )

        # Сохранить изменения
        await session.commit()
        return True

    except Exception as e:
        # Логирование ошибки (если нужно)
        print(f"Ошибка обновления параметра: {e}")
        await session.rollback()
        return False


@connection
async def get_param(telegram_id: int, param: str, session: AsyncSession):
    """
    Получение значения параметра по `telegram_id` из таблицы User.

    Args:
        telegram_id (int): Telegram ID пользователя.
        param (str): Название параметра, который нужно получить.
        session (AsyncSession): Сессия для работы с базой данных.

    Returns:
        значение параметра, либо None, если пользователь или параметр не найден.
    """
    try:
        # Выполнить запрос на получение объекта User по telegram_id
        res = await session.execute(
            select(getattr(User, param)).where(User.telegram_id == telegram_id)
        )
        result = res.scalar()
        return result
    except AttributeError:
        raise ValueError(f"Параметр '{param}' не найден в модели User.")



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
