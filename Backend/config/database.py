from os import environ

from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

print(environ.get("PRODUCTION"))

if production := environ.get("PRODUCTION", False):
    host = environ.get("DB_HOST")
    port = environ.get("DB_PORT", 5432)
    username = environ.get("DB_USER")
    password = environ.get("DB_PASSWORD")
    database = environ.get("DB_NAME")
else:
    config = dotenv_values(".env")

    host = config["IP"]
    port = config["PORT"]
    username = config["USERNAME"]
    password = config["PASSWORD"]
    database = config["DATABASE"]

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
