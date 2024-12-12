from src.database.database import async_session_maker, Base, engine


# Асинхронная функция для добавления пользователя
async def add_person(user):
    try:
        async with async_session_maker() as session:
            async with session.begin():
                session.add(user)
            await session.refresh(user)
            print(f"Added user: {user}")
            return user
    except Exception as e:
        print(f"Error adding user: {e}")

async def reset_database():
    # Удаляем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Создаем все таблицы заново
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)