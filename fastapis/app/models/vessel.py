from datetime import date
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Vessel(SQLModel, table=True):
    __tablename__ = "vessels"  # 显式指定表名
    
    vessel_id: int = Field(default=None, primary_key=True)
    name: str
    model: str = None
    registration_date: date = Field(default_factory=date.today)
    company_id: int = Field(default=None, foreign_key="companies.company_id")


# 创建船舶请求体
class VesselCreate(SQLModel):
    name: str
    model: Optional[str] = None
    registration_date: Optional[date] = None
    company_id: Optional[int] = None

# 更新船舶请求体
class VesselUpdate(SQLModel):
    name: Optional[str] = None
    model: Optional[str] = None
    registration_date: Optional[date] = None
    company_id: Optional[int] = None

class VesselResponse(BaseModel):
    vessel_id: int
    name: str
    model: Optional[str]
    registration_date: date  # 修改为 date 类型
    company_id: Optional[int]

    class Config:
        orm_mode = True

