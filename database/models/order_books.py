from sqlalchemy import Table, Column, ForeignKey
from database.connection import Base

order_books = Table(
    "order_books", Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)