from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(foreign_key="orders.id")
    total: Mapped[float] = mapped_column()
    