from sqlalchemy import MetaData, Table, Column, BIGINT, Integer, String, Text, DateTime, Boolean, ForeignKey, SmallInteger
metadata = MetaData()

# Define the user table
user = Table('user', metadata,
             Column('user_id', BIGINT(), primary_key=True),
             Column('first_name', Text()),
             Column('last_name', Text()),
             Column('sex', Integer()),  # 0, 1 as female - male relationship to save some data
             Column('age', Integer()),
             Column('date_of_birth', DateTime()),
             Column('telegram_id', BIGINT(), unique=True),
             Column('email', Text()),
             Column('city', Text()),
             Column('geolocation', Text()),
             Column('privileges', Text()),
             Column('status', Integer())  # 3 modes: inactive, in search, in game
             )

# Define the in_game_user table
in_game_user = Table('in_game_user', metadata,
                     Column('user_id', BIGINT(), ForeignKey('user.user_id'), primary_key=True),
                     Column('user_health_points', BIGINT()),
                     Column('user_exp', BIGINT()),
                     Column('user_money_gold', BIGINT()),
                     Column('user_money_silver', BIGINT()),
                     Column('user_money_bronze', BIGINT()),
                     Column('is_adult', Boolean())
                     )

# Define the user_statistics table
user_statistics = Table('user_statistics', metadata,
                        Column('user_id', BIGINT(), ForeignKey('user.user_id'), primary_key=True),
                        Column('endgames', Integer()),
                        Column('done_quests', Integer()),
                        Column('declined_challenges', Integer()),
                        Column('reports', Integer())
                        )

#photos = Table('photos', metadata




sessions = Table('session', metadata,
                Column('host_id', BIGINT(), ForeignKey('user.user_id'), primary_key=True),
                    Column('players quantity', SmallInteger()),
                    Column('status', Boolean()), # open / closed / paused ?
                    Column('passowrd', Integer()),
                    Column('status', Boolean()),
                    Column('is_adm', Boolean()),
                    Column("players", Text()),
                    Column("created_at", DateTime())
                    Column("")
               )