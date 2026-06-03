import json
from sqlalchemy.orm import Session
from database.connection import engine, Base
from database.models.book import Book

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with open("books.json") as f:
    data = json.load(f)

with Session(engine) as session:
    for item in data:
        book = Book(
            isbn=item["isbn"],
            title=item["title"],
            author=item["author"],
            price=item["price"],
            stock=item["stock"],
            book_type=item["book_type"]
        )
        session.add(book)
    session.commit()

print(f"Seeded {len(data)} books!")