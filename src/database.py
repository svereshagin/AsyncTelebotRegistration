from sqlalchemy import create_engine
from config import DB_CONFIG


engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
    echo=True, pool_size=6, max_overflow=10, encoding='latin1'
)
engine.connect()

print(engine)