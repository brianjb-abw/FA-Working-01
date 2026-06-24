from fastapi import Body, FastAPI

# base url:  127.0.0.1:8000

app = FastAPI()                     


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Two', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author One', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/")                      
async def api_root():              
    return {'message': 'ok'}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book 
    
    # if didn't find book
    return {'message': 'book not found'}    


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = [
        b for b in BOOKS if b['category'].casefold()==category.casefold()
    ]
    return books_to_return


@app.get("/books/for_author/")
async def get_books_for_author(author: str):
    books_to_return = []
    for b in BOOKS:
        if b.get('author').casefold() == author.casefold():
            books_to_return.append(b)
    
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    
    for b in BOOKS:
        if b.get('author').casefold() == book_author.casefold() and \
            b.get('category').casefold() == category.casefold():
                books_to_return.append(b)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

    if new_book in (BOOKS):
        return new_book
    else:
        return {'message': 'error'}


@app.put("/books/update_book")
async def update_book(edit_items=Body()):

    for b in BOOKS:
        if b.get('title').casefold() == edit_items.get('title').casefold():
            for k in edit_items.keys():
                if k != 'title':
                    b[k] = edit_items[k]

            return b

    return {"message": f"book '{edit_items['title']}' not found"}


@app.delete("/books/remove_book/")
async def remove_book(book_title: str):
    for b in BOOKS:
        if b['title'].casefold() == book_title.casefold():
            BOOKS.remove(b)
            return {"message": f"book '{book_title}' removed"}
    
    return {"message": f"book '{book_title}' not found"}

