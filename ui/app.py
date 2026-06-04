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
        
        nav = tk.Frame(self)
        nav.pack(side=tk.TOP, fill=tk.X)

        tk.Button(nav, text="Catalogue", command=lambda: self.bring_view_to_front(CatalogueView)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Cart", command=lambda: self.bring_view_to_front(CartView)).pack(side=tk.LEFT, padx=10, pady=10)

        # Creation of parent container
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Makes container responsive
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize shopping cart, must be done before views are created so CartView can access it.
        self.cart = ShoppingCart()

        # initialize views
        self.views = {}

        for View in (CatalogueView, CartView):
            view = View(self.container, self)
            self.views[View] = view
            view.grid(row=0, column=0, sticky="nsew")

        self.bring_view_to_front(CatalogueView)
        
    
    def bring_view_to_front(self, view):
        self.views[view].tkraise()
        if view == CartView:
            self.views[CartView].refresh_cart()
            self.views[CartView].total_label.config(text=f"Total: ${self.cart.calculate_total():.2f}")


class CatalogueView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tree = ttk.Treeview(self, columns=("ISBN", "Title", "Author", "Price", "Stock", "Type"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_books()
        self.tree.bind("<Double-1>", self.add_to_cart)
        self.tree.bind("<Shift-Double-1>", self.remove_from_cart)

    def load_books(self):
        with Session(engine) as session:
            books = session.query(Book).all()
            # Printing for debugging
            print(f"Loaded {len(books)} books from the database.")
            for book in books:
                self.tree.insert("", tk.END, values=(book.isbn, book.title, book.author, book.price, book.stock, book.book_type))
    
    def add_to_cart(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0])["values"]
            isbn = item_values[0]
            with Session(engine) as session:
                book = session.query(Book).filter_by(isbn=isbn).first()
                if book:
                    self.controller.cart.add_book(book)
                    print(f"Added {book.title} to cart.")
                    
    def remove_from_cart(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0])["values"]
            isbn = item_values[0]
            with Session(engine) as session:
                book = session.query(Book).filter_by(isbn=isbn).first()
                if book:
                    self.controller.cart.remove_book(book)
                    print(f"Removed {book.title} from cart.")

class CartView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tree = ttk.Treeview(self, columns=("ISBN", "Title", "Author", "Quantity"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.total_label = tk.Label(self, text="Total: $0.00")
        self.total_label.pack(pady=10)
        self.checkout_button = tk.Button(self, text="Checkout", command=self.controller.cart.checkout)
        self.checkout_button.pack(pady=10)
        
        for book, quantity in self.controller.cart.books:
            self.tree.insert("", tk.END, values=(book.isbn, book.title, book.author, quantity))

    def refresh_cart(self):
        # Printing for debugging
        print(f"Loading {len(self.controller.cart.books)} items into the cart.")
        print(f"Loading cart items: {[book.title for book, quantity in self.controller.cart.books]}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book, quantity in self.controller.cart.books:
            self.tree.insert("", tk.END, values=(book.isbn, book.title, book.author, quantity))
        self.total_label.config(text=f"Total: ${self.controller.cart.calculate_total():.2f}")