from typing import List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        'id': 1,
        'title': 'Think Python',
        'author': 'Allen B Downey',
        'publisher': "O'Reilly Media",
        'page_count': 1234,
        'published_date': '2001-01-01',
        'language': 'English'
    },
    {
        'id': 2,
        'title': 'Django By Example',
        'author': 'Antonio Balle',
        'publisher': "Packt Publishing Ltd",
        'page_count': 1023,
        'published_date': '2002-01-29',
        'language': 'English'
    },
    {
        'id': 3,
        'title': 'The Web Socket HandBook',
        'author': 'Alex Diacomu',
        'publisher': "Xinyu Wang",
        'page_count': 3677,
        'published_date': '2001-01-01',
        'language': 'English'
    },
    {
        'id': 4,
        'title': 'Read First Javascript',
        'author': 'Hellen Smith',
        'publisher': "Oreilly Media",
        'page_count': 540,
        'published_date': '2001-01-01',
        'language': 'English'
    },
]

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: str
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

@app.get('/books', response_model=List[Book])
async def all_books():
    return books

@app.get('/books/{book_id}')
async def single_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'Book Was Not Found, Please Try Another Book!'
    )


@app.post('/books', status_code = status.HTTP_201_CREATED)
async def create_book(data: Book) -> dict:
    new_book = data.model_dump()
    
    books.append(new_book)

    return new_book


@app.patch('/books/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'Was Not Possible To Foud The Book!'
    )
    

@app.delete('/books/{book_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

        return {}

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'Book Was Not Found, Please Try Another Book!'
    )
