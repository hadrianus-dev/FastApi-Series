from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book

class BookService:

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
            
        return result.scalars().all()


    async def get_one_book(self, session: AsyncSession, book_uid: str, as_dict: bool = True) -> dict | None:
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        book = result.scalars().first()
        if as_dict:
            return book.model_dump() if book is not None else None
        return book


    async def create_book(self, session: AsyncSession, book_data: BookCreateModel):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(
            book_data_dict['published_date'], "%Y-%m-%d"
        ).date()
        session.add(new_book)
        await session.commit()
        return new_book.model_dump()


    async def update_book(self, session: AsyncSession, book_uid: str, book_data: BookUpdateModel):
        book_to_update = await self.get_one_book(session, book_uid, as_dict=False)
        if book_to_update is not None:
            book_data_dict = book_data.model_dump()
            for key, value in book_data_dict.items():
                setattr(book_to_update, key, value)
            session.add(book_to_update)
            await session.commit()
            return book_to_update.model_dump()
        return None


    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_to_delete = await self.get_one_book(session, book_uid, as_dict=False)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return {"message": "Book deleted successfully"}
        return None

