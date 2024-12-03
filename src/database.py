from sqlalchemy import create_engine
from config import DB_CONFIG
from models import metadata

try:
    # Создание движка
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
        echo=True, pool_size=6, max_overflow=10)

    # Подключение к базе данных
    connection = engine.connect()

    # Создание всех таблиц
    metadata.create_all(engine)
    print("Таблицы успешно созданы.")

except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    # Закрытие соединения
    if 'connection' in locals():
        connection.close()
        print("Соединение закрыто.")
