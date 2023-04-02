from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, scoped_session

username = "kallox"
password = "Claudioxx124"
database = "inventory"
ip = "localhost"
port = 5432

DATABASE_URL = f"postgresql://{username}:{password}@{ip}:{port}/{database}"
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
#Session = scoped_session(session_factory)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#def get_session(): 
    #return Session
