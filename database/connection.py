from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "sqlite:///bookstore.db"

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass