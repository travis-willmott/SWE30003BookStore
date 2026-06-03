import tkinter as tk
import tkinter.ttk as ttk
from database.connection import engine, Base, Session
from database.models import Book

Base.metadata.create_all(engine)

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bookstore")
        self.tree = ttk.Treeview(root, columns=("ISBN", "Title", "Author", "Price", "Stock", "Type"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_books()

    def load_books(self):
        with Session(engine) as session:
            books = session.query(Book).all()
            print(f"Loaded {len(books)} books from the database.")
            for book in books:
                self.tree.insert("", tk.END, values=(book.isbn, book.title, book.author, book.price, book.stock, book.book_type))