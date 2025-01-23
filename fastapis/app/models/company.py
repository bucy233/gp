from datetime import datetime

from sqlmodel import Field, SQLModel


# 公司表模型
class Company(SQLModel, table=True):
    __tablename__ = "companies"

    company_id: int = Field(default=None, primary_key=True)
    name: str
    address: str | None = None
    contact: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"})

                    