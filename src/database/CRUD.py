import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def main():
    async with async_session_maker() as session:
        # Create
        user = await create_user(session, "test_user", "test@example.com", "securepass")
        print(f"Created User: {user}")

        # Read
        fetched_user = await get_user_by_email(session, "test@example.com")
        print(f"Fetched User: {fetched_user}")

        # Update
        updated_user = await update_user_email(session, user.id, "new_email@example.com")
        print(f"Updated User: {updated_user}")

        # Delete
        deleted = await delete_user(session, user.id)
        print(f"Deleted User: {deleted}")
#сделать логгер под них
# Запуск приложения
asyncio.run(main())


async def delete_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False

class CRUD:
    async def get_user_by_id(session: AsyncSession, user_id: int):
        return await session.get(User, user_id)



    # async def update_user_email(User, session: AsyncSession, user_id: int, new_email: str):
    #     user = await session.get(User, user_id)
    #     if user:
    #         user.email = new_email
    #         await session.commit()
    #         await session.refresh(user)
    #         return user
    #     return None

# Чтение записи по ID
    async def get_user_by_id(session: AsyncSession, user_id: int):
        return await session.get(User, user_id)

# Чтение записи по email
#     async def get_user_by_email(session: AsyncSession, email: str):
#         stmt = select(User).where(User.email == email)
#         result = await session.execute(stmt)
#         return result.scalar_one_or_none()  # Возвращает объект или None


    async def create_user(session: AsyncSession, username: str, email: str, password: str):
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # Обновляем объект с данными из БД
        return new_user