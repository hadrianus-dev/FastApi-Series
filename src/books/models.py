from datetime import date, datetime
from typing import Any
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid4(), nullable=False)
    )
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: date
    language: str
    created_at: datetime = Field(
        sa_column=Column(
            "created_at", pg.TIMESTAMP, default=datetime.now(), nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            "updated_at", pg.TIMESTAMP, default=datetime.now(), nullable=False
        )
    )

    class Config:
        orm_mode = True

    def __reduce__(self) -> str | tuple[Any, ...]:
        return super().__reduce__()

    def __repr__(self) -> str:
        return f"<Book {self.title} >"
