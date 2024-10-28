from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel
from src.books.data import books

book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def all_books():
    return books


@book_router.get("/{book_id}")
async def single_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Was Not Found, Please Try Another Book!",
    )


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(data: Book) -> dict:
    new_book = data.model_dump()

    books.append(new_book)

    return new_book


@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Was Not Possible To Foud The Book!",
    )


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

        return {}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book Was Not Found, Please Try Another Book!",
    )
