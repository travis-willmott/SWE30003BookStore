from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database.connection import Base

class OrderBook(Base):
    __tablename__ = "order_books"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    book_isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1)