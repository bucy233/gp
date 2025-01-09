from app.core.db import get_db_session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from fastapi import Depends, HTTPException
from sqlmodel import Session


class CompanyService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_companies(self) -> list[Company]:
        return self.session.query(Company).all()

    def get_company_by_id(self, company_id: int) -> Company:
        company = self.session.get(Company, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="公司不存在")
        return company

    def create_company(self, company_to_create: CompanyCreate) -> Company:
        company = Company.from_orm(company_to_create)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def update_company(self, company_id: int, company_update: CompanyUpdate) -> Company:
        db_company = self.get_company_by_id(company_id)
        if company_update.name:
            db_company.name = company_update.name
        if company_update.address:
            db_company.address = company_update.address
        if company_update.contact:
            db_company.contact = company_update.contact
        self.session.commit()
        self.session.refresh(db_company)
        return db_company

    def delete_company(self, company_id: int) -> Company:
        db_company = self.get_company_by_id(company_id)
        self.session.delete(db_company)
        self.session.commit()
        return db_company

# 获取服务实例
def get_company_service(session: Session = Depends(get_db_session)):
    return CompanyService(session)
