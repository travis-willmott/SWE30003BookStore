from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base
from database.models import Book

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    total: Mapped[float] = mapped_column()
    
    books: Mapped[list[Book]] = relationship(secondary="order_books")
