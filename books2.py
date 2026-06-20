from fastapi import FastAPI, Body


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


BOOKS = [
    Book(1, 'The art of sloth', 'doogie', 'those who eschew laziness are doing it wrong', 4),
    Book(2, 'Cooking with potato chips', 'doogie', 'a helpful couch potato skill', 2),
    Book(3, 'Dark web skills', 'cryptique', 'no desc, you are either in or not', 5),
    Book(4, 'Foz on the law', 'Anderson Fozworth', 'foz weighs in on 2026 new issues', 4),
    Book(5, 'Lost TV classics', 'bob', 'shows that you forgot you forgot', 5),
    Book(6, 'The art of being an a-hole', 'Anderson Fozworth', 'how to provoke sue-able offenses', 3)
]


# ---- Root
@app.get("/")                      
async def api_root():              
    return "ok"


# ---- Get all books
@app.get("/books")
async def get_all_books():
    return BOOKS


# ---- Post Book
@app.post("/create_book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)
    return {
        "message": "book added",
        "book": book_request
    }