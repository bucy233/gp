from typing import Optional

from pydantic import BaseModel


class VesselCreate(BaseModel):
    name: str
    model: Optional[str]
    company_id: Optional[int]

class VesselUpdate(BaseModel):
    name: Optional[str]
    model: Optional[str]
    company_id: Optional[int]

class VesselResponse(BaseModel):
    vessel_id: int
    name: str
    model: Optional[str]
    registration_date: str
    company_id: Optional[int]

    class Config:
        orm_mode = True
