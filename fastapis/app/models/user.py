from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# 用户表模型
class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(default=None, primary_key=True)
    name: str
    role: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 创建用户请求体
class UserCreate(SQLModel):
    name: str
    role: str
    email: EmailStr
    password: str

# 登录请求体
class UserLogin(SQLModel):
    email: EmailStr
    password: str

# 更新用户请求体
class UserUpdate(SQLModel):
    name: str | None = None
    role: str | None = None
    email: EmailStr | None = None
    password: str | None = None
