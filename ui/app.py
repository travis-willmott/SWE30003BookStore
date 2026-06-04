import tkinter as tk
import tkinter.ttk as ttk
from database.connection import engine, Base, Session
from database.models import Book
from ui.cart import ShoppingCart

Base.metadata.create_all(engine)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Glenferrie Book Store")
        self.geometry("800x600")
        
        # Creation of parent container
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Makes container responsive
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initialize views
        self.views = {}

        for View in (CatalogueView, CartView):
            view = View(self.container, self)
            self.views[View] = view
            view.grid(row=0, column=0, sticky="nsew")

        self.bring_view_to_front(CatalogueView)
        self.cart = ShoppingCart()
        
    
    def bring_view_to_front(self, view):
        self.views[view].tkraise()


class CatalogueView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tree = ttk.Treeview(self, columns=("ISBN", "Title", "Author", "Price", "Stock", "Type"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_books()
        self.tree.bind("<<TreeviewSelect>>", self.click_row)

    def load_books(self):
        with Session(engine) as session:
            books = session.query(Book).all()
            print(f"Loaded {len(books)} books from the database.")
            for book in books:
                self.tree.insert("", tk.END, values=(book.isbn, book.title, book.author, book.price, book.stock, book.book_type))
    
    def click_row(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0])["values"]
            isbn = item_values[0]
            with Session(engine) as session:
                book = session.query(Book).filter_by(isbn=isbn).first()
                if book:
                    self.controller.cart.add_book(book)
                    print(f"Added {book.title} to cart.")

class CartView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller