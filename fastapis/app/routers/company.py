from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.sercices.company import CompanyService, get_company_service
from fastapi import APIRouter, Depends

router = APIRouter()

# 获取所有公司
@router.get("/companies", response_model=list[CompanyResponse])
async def get_companies(service: CompanyService = Depends(get_company_service)):
    return service.get_all_companies()

# 获取单个公司
@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, service: CompanyService = Depends(get_company_service)):
    return service.get_company_by_id(company_id)

# 创建公司
@router.post("/companies", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, service: CompanyService = Depends(get_company_service)):
    return service.create_company(company)

# 更新公司信息
@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: int, company: CompanyUpdate, service: CompanyService = Depends(get_company_service)):
    return service.update_company(company_id, company)

# 删除公司
@router.delete("/companies/{company_id}", response_model=CompanyResponse)
async def delete_company(company_id: int, service: CompanyService = Depends(get_company_service)):
    return service.delete_company(company_id)
