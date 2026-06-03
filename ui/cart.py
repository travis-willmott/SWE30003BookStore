from sqlalchemy.orm import Session
from database.models import Book, Order
class ShoppingCart:
    def __init__(self):
        self.books: list[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        self.books.remove(book)

    def calculate_total(self) -> float:
        return sum(book.price for book in self.books)
    
    def checkout(self, session: Session):
        total = self.calculate_total()
        order = Order(total=total, books=self.books)
        session.add(order)
        session.commit()