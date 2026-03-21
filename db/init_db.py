import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DB_NAME = "it_cube_project.db"


# Функция, если БД должна лежать рядом с проектом

# def get_db_path():
#     # если запущено как exe
#     if getattr(sys, "frozen", False):
#         base_dir = os.path.dirname(sys.executable)
#     else:
#         base_dir = os.path.abspath(".")
#     return os.path.join(base_dir, DB_NAME)


def get_db_path():
    # Базовая папка, где должна лежать БД
    base_dir = r"C:\Users\Public\Documents\it_cube_project"

    # Создаём папку, если её нет
    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, DB_NAME)


DATABASE_URL = f"sqlite:///{get_db_path()}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

Session = sessionmaker(bind=engine)


def create_database():
    Base.metadata.create_all(engine)
    print("База данных и таблицы созданы успешно!")
