from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Book(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: str
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
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