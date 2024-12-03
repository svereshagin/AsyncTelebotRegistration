from sqlalchemy import MetaData, Table, String, BIGINT, Integer, Column, Text, DateTime, Boolean

metadata = MetaData()

user = Table('user', metadata,
             Column('user_id', BIGINT(), primary_key=True),
             Column('first_name', Text()),
             Column('last_name', Text() ),
             Column('sex', Integer()), #0, 1 as female - male relationship to save some data
             Column('age', Integer()),
             Column('date_of_birth', DateTime()),
             Column('telegram_id', BIGINT(), unique=True),
             Column('email', Text()),
             )

