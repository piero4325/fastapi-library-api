from fastapi import FastAPI, HTTPException, Depends
from app.db import get_db_connection, close_db_connection
from app.schemas import AuthorCreate, AuthorResponse, BookCreate, BookResponse

app = FastAPI(title="Library API")

def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        close_db_connection(conn)

@app.get("/authors", response_model=list[AuthorResponse])
def get_authors(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, country FROM authors ORDER BY id")
    authors = cursor.fetchall()
    cursor.close()
    return [dict(author) for author in authors]

@app.post("/authors", response_model=AuthorResponse, status_code=201)
def create_author(author: AuthorCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO authors (name, country) VALUES (%s, %s) RETURNING id, name, country",
        (author.name, author.country)
    )
    db.commit()
    new_author = dict(cursor.fetchone())
    cursor.close()
    return new_author

@app.get("/books", response_model=list[BookResponse])
def get_books(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, title, year, author_id FROM books ORDER BY id")
    books = cursor.fetchall()
    cursor.close()
    return [dict(book) for book in books]

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, year, author_id) VALUES (%s, %s, %s) RETURNING id, title, year, author_id",
        (book.title, book.year, book.author_id)
    )
    db.commit()
    new_book = dict(cursor.fetchone())
    cursor.close()
    return new_book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE books SET title=%s, year=%s, author_id=%s WHERE id=%s RETURNING id, title, year, author_id",
        (book.title, book.year, book.author_id, book_id)
    )
    db.commit()
    updated_book = cursor.fetchone()
    cursor.close()
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(updated_book)

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    db.commit()
    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.close()