from sqlalchemy.orm import Mapped, mapped_column
from database.connection import Base

class Book(Base):
    __tablename__ = "books"
    isbn: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    book_type: Mapped[str]