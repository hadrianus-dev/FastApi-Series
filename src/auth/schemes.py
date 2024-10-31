from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class UserSchema(BaseModel):
    uid: UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)
    first_name: Optional[str]
    last_name: Optional[str]


class UserUpdateSchema(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: Optional[bool] = Field(default=False)


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)
