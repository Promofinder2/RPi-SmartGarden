from enum import auto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sensor_database.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = scoped_session(sessionmaker(bind=engine,autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = SessionLocal.query_property()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()