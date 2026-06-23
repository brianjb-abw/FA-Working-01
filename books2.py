from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed for create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "a new book",
                "author": "joseph smith",
                "description": "description of new book",
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(1, 'The art of sloth', 'doogie', 'those who eschew laziness are doing it wrong', 4),
    Book(2, 'Cooking with potato chips', 'doogie', 'a helpful couch potato skill', 2),
    Book(3, 'Dark web skills', 'cryptique', 'no desc, you are either in or not', 5),
    Book(4, 'Foz on the law', 'Anderson Fozworth', 'foz weighs in on 2026 new issues', 4),
    Book(5, 'Lost TV classics', 'bob', 'shows that you forgot you forgot', 5),
    Book(6, 'The art of being an a-hole', 'Anderson Fozworth', 'how to provoke sue-able offenses', 3)
]

#   ** Next ID
def get_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book



# ---- Root/Test
@app.get("/")                      
async def api_root():              
    return "ok"


# ---- Get all books
@app.get("/books")
async def get_all_books():
    return BOOKS


# ---- Get single book
@app.get("/books/{book_id}")
async def get_single_book(book_id: int):
    book_to_ret = [b for b in BOOKS if b.id==book_id]
    if len(book_to_ret) > 0:
        return book_to_ret[0]
    else:
        return {"message": f"book {book_id} not found"}


# ---- Get books by rating
@app.get("/books/")
async def get_book_by_rating(book_rating: int):
    books_to_return = [b for b in BOOKS if b.rating == book_rating]

    return books_to_return


# ---- Post Book
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(get_book_id(new_book))
    return {
        "message": "book added",
        "book": new_book
    }


# ---- Put Book Update
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"message": f"book {book.id} updated", "book": book}
    
    # not found
    return {"message": f"book {book.id} not found - no update"}


# ---- Delete Book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for b in BOOKS:
        if b.id == book_id:
            BOOKS.remove(b)

            return {"message": f"book {book_id} deleted"}

    # not found
    return {"message": f"book {book_id} not found - no delete"}
