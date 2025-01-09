from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    role: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
