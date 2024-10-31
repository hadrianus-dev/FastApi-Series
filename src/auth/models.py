from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid4(), nullable=False)
    )
    username: str = Field(str, nullable=False, unique=True, index=True)
    email: str = Field(str, nullable=False, unique=True)
    password: str = Field(str, nullable=False, unique=True, exclude=True)
    first_name: str = Field(str, nullable=True)
    last_name: str = Field(str, nullable=True)
    is_verified: bool = Field(default=False)
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

    def __repr__(self) -> str:
        return f"<User {self.username} >"
