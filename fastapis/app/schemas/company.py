from datetime import datetime

from pydantic import BaseModel


# 创建公司请求体
class CompanyCreate(BaseModel):
    name: str
    address: str | None = None
    contact: str | None = None

# 更新公司请求体
class CompanyUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    contact: str | None = None

# 公司响应体（返回数据库字段）
class CompanyResponse(CompanyCreate):
    company_id: int
    created_at: datetime
