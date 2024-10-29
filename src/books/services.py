from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book

class BookService:

    async def get_all_books(self, session: AsyncSession):
        try:
            statement = select(Book).order_by(desc(Book.created_at))
            result = await session.execute(statement)
            
            #return result.scalars().all()
            return result.all()
        except Exception as exception:
            raise exception


    async def get_one_book(self, session: AsyncSession, book_uid: str):
        try:
            statement = select(Book).where(Book.uid == book_uid)
            result = await session.execute(statement)
            #return result.scalars().first()
            book = result.first()
            return book if book is not None else None
        except Exception as exception:
            raise exception


    async def create_book(self, session: AsyncSession, book_data: BookCreateModel):
        try:
            book_data_dict = book_data.model_dump()
            new_book = Book(**book_data_dict)
            new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
            session.add(new_book)
            await session.commit()
            return new_book
        except Exception as exception:
            raise exception


    async def update_book(self, session: AsyncSession, book_uid: str, book_data: BookUpdateModel):
        try:
            book_to_update = await self.get_one_book(session, book_uid)
            if book_to_update is not None:
                book_data_dict = book_data.model_dump()

                for key, value in book_data_dict.items():
                    setattr(book_to_update, key, value)

                session.add(book_to_update)
                await session.commit()
                return book_to_update    

            return None
        except Exception as exception:
            raise exception 

    async def delete_book(self, session: AsyncSession, book_uid: str):
        try:
            book_to_delete = await self.get_one_book(session, book_uid)

            if book_to_delete is not None:
                await session.delete(book_to_delete)
                await session.commit()
                return {}

            return None
        except Exception as exception:
            raise exception

