from app.core.db import get_db_session
from app.models.vessel import VesselCreate, VesselResponse, VesselUpdate
from app.sercices.vessel import VesselService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=VesselResponse)
async def create_vessel(vessel: VesselCreate, db: Session = Depends(get_db_session)):
    service = VesselService(db)
    if not vessel.company_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="必须提供公司ID")
    return service.create_vessel(vessel)

@router.get("/{vessel_id}", response_model=VesselResponse)
async def get_vessel(vessel_id: int, db: Session = Depends(get_db_session)):
    service = VesselService(db)
    return service.get_vessel_by_id(vessel_id)

@router.put("/{vessel_id}", response_model=VesselResponse)
async def update_vessel(vessel_id: int, vessel: VesselUpdate, db: Session = Depends(get_db_session)):
    service = VesselService(db)
    return service.update_vessel(vessel_id, vessel)

@router.delete("/{vessel_id}")
async def delete_vessel(vessel_id: int, db: Session = Depends(get_db_session)):
    service = VesselService(db)
    service.delete_vessel(vessel_id)
    return {"message": "删除成功"}

@router.get("/", response_model=list[VesselResponse])
async def list_vessels(db: Session = Depends(get_db_session)):
    service = VesselService(db)
    return service.get_all_vessels()
