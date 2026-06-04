from sqlalchemy.orm import Session
from database.models import Book, Order
class ShoppingCart:
    def __init__(self):
        self.books: list[tuple[Book, int]] = []

    def add_book(self, book: Book):
        # Check if the book is already in the cart
        for i, (b, quantity) in enumerate(self.books):
            if b.isbn == book.isbn:
                self.books[i] = (b, quantity + 1)
                return
        self.books.append((book, 1))

    def remove_book(self, book: Book):
        for i, (b, quantity) in enumerate(self.books):
            if b.isbn == book.isbn:
                if quantity > 1:
                    self.books[i] = (b, quantity - 1)
                else:
                    self.books.pop(i)
                return

    def calculate_total(self) -> float:
        return sum(book.price * quantity for book, quantity in self.books)

    def checkout(self, session: Session):
        total = self.calculate_total()
        order = Order(total=total, books=self.books)
        session.add(order)
        session.commit()