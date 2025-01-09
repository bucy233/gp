from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# 用户模型
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    user_id: int = Field(default=None, primary_key=True)
    name: str
    role: str
    email: EmailStr
    password: str  # 加密存储的密码
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 创建用户请求体
class UserCreate(SQLModel):
    name: str
    role: str
    email: EmailStr
    password: str

# 更新用户请求体
class UserUpdate(SQLModel):
    name: Optional[str] = None  # 使用 Optional 来表示可选字段
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# 用户登录请求体
class UserLogin(SQLModel):
    email: EmailStr
    password: str
