from datetime import date
from typing import Optional

from pydantic import BaseModel


class MaintenanceSchema(BaseModel):
    id: Optional[int] = None
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str
    equiptment_id: int

    class Config:
        from_attributes = True


class MaintenanceFromEquipment(BaseModel):
    id: int
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str
    equiptment_id: int

    class Config:
        from_attributes = True


class EditMaintenanceSchema(BaseModel):
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str

    class Config:
        from_attributes = True
