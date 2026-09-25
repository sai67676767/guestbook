import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Читаем переменные окружения (они передаются из .env через docker-compose)
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Формируем строку подключения к PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Фабрика сессий — через неё будем делать запросы к БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для наших моделей
Base = declarative_base()


# Функция-зависимость для FastAPI: открывает сессию и закрывает её после запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

