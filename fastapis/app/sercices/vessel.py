from app.core.db import get_db_session
from app.models.vessel import Vessel, VesselCreate, VesselUpdate
from fastapi import Depends, HTTPException
from sqlmodel import Session


class VesselService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_vessels(self) -> list[Vessel]:
        return self.session.query(Vessel).all()

    def get_vessel_by_id(self, vessel_id: int) -> Vessel:
        vessel = self.session.get(Vessel, vessel_id)
        if not vessel:
            raise HTTPException(status_code=404, detail="船舶不存在")
        return vessel

    def create_vessel(self, vessel_data: VesselCreate) -> Vessel:
        vessel = Vessel(**vessel_data.dict())
        self.session.add(vessel)
        self.session.commit()
        self.session.refresh(vessel)
        return vessel
    
    def update_vessel(self, vessel_id: int, vessel_update: VesselUpdate) -> Vessel:
        db_vessel = self.get_vessel_by_id(vessel_id)
        if vessel_update.name:
            db_vessel.name = vessel_update.name
        if vessel_update.model:
            db_vessel.model = vessel_update.model
        if vessel_update.registration_date:
            db_vessel.registration_date = vessel_update.registration_date
        if vessel_update.company_id:
            db_vessel.company_id = vessel_update.company_id
        self.session.commit()
        self.session.refresh(db_vessel)
        return db_vessel

    def delete_vessel(self, vessel_id: int) -> Vessel:
        db_vessel = self.get_vessel_by_id(vessel_id)
        self.session.delete(db_vessel)
        self.session.commit()
        return db_vessel

def get_vessel_service(session: Session = Depends(get_db_session)):
    return VesselService(session)