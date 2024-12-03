from sqlalchemy import MetaData, Table, String, BIGINT, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

metadata = MetaData()

user = Table('user', metadata,
             Column('user_id', BIGINT(), primary_key=True),
             Column('first_name', BIGINT(), primary_key=True),
             Column('last_name', Integer(), primary_key=True),
             Column('sex', Integer(), primary_key=True),
             Column('age', Integer(), primary_key=True),
             Column('date_of_birth', Integer(), primary_key=True),
             Column('telegram_id', Integer(), primary_key=True),
             Column('email', Integer(), primary_key=True),
             )