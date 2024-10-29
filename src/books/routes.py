from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from src.database.main import get_session
from src.books.services import BookService
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
#from src.books.models import Book

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=List[Book])
async def all_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/{book_uid}")
async def single_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_one_book(session, book_uid)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Was Not Found, Please Try Another Book!",
        )


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.create_book(session, data)
    return book


@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(session, book_uid, book_update_data)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Was Not Possible To Foud The Book!",
        )


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> None:
    if not await book_service.delete_book(session, book_uid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Was Not Found, Please Try Another Book!",
        )
        
