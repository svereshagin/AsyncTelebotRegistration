from sqlalchemy import (MetaData, Table, Column, BIGINT,
                        Integer, String, Text, DateTime,
                        Boolean, ForeignKey, SmallInteger)
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession,create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

class Base(AsyncAttrs, DeclarativeBase):
    pass

metadata = MetaData()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BIGINT(), primary_key=True)
    first_name = Column(Text())
    last_name = Column(Text())
    sex = Column(Integer())  # 0 - female, 1 - male
    age = Column(Integer())
    date_of_birth = Column(DateTime())
    telegram_id = Column(BIGINT(), unique=True)
    email = Column(Text())
    city = Column(Text())
    geolocation = Column(Text())
    privileges = Column(Text())
    status = Column(Integer())  # 0: inactive, 1: in search, 2: in game

    # Relationships
    in_game_user = relationship("InGameUser ", back_populates="user")
    user_statistics = relationship("User Statistics", back_populates="user")
    sessions = relationship("Session", back_populates="host")

class InGameUser (Base):
    __tablename__ = 'in_game_users'

    user_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
    user_health_points = Column(BIGINT())
    user_exp = Column(BIGINT())
    user_money_gold = Column(BIGINT())
    user_money_silver = Column(BIGINT())
    user_money_bronze = Column(BIGINT())
    is_adult = Column(Boolean())

    # Relationships
    user = relationship("User ", back_populates="in_game_user")

class UserStatistics(Base):
    __tablename__ = 'user_statistics'

    user_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
    endgames = Column(Integer())
    done_quests = Column(Integer())
    declined_challenges = Column(Integer())
    reports = Column(Integer())

    # Relationships
    user = relationship("User ", back_populates="user_statistics")

class Session(Base):
    __tablename__ = 'sessions'

    host_id = Column(BIGINT(), ForeignKey('users.user_id'), primary_key=True)
    players_quantity = Column(SmallInteger())
    status = Column(Boolean())
    password = Column(Integer())
    is_adm = Column(Boolean())
    players = Column(Text())
    created_at = Column(DateTime())

    # Relationships
    host = relationship("User ", back_populates="sessions")

def run_queries(session):
    """A function written in "synchronous" style that will be invoked
       within the asyncio event loop.
       The session object passed is a traditional orm.Session object with
       synchronous interface.
       stmt — это объект запроса, который выбирает все записи из таблицы,
       соответствующей модели A. select(A) создает SQL-запрос для извлечения
       всех строк из таблицы, связанной с классом A."""
    stmt = select(A)

    result = session.execute(stmt)

    for a1 in result.scalars():
        print(a1)
        # lazy loads
        for b1 in a1.bs:
            print(b1)

    result = session.execute(select(A).order_by(A.id))

    a1 = result.scalars().first()

    a1.data = "new data"


async def async_main():
    """Main program function."""

    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        # we have the option to run a function written in sync style
        # within the AsyncSession.run_sync() method.  The function will
        # be passed a synchronous-style Session object and the function
        # can use traditional ORM patterns.
        await session.run_sync(run_queries)

        await session.commit()


asyncio.run(async_main())
