from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MaintenanceSchema(BaseModel):
    id: Optional[int] = None
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str
    equiptment_id: int

    model_config = ConfigDict(from_attributes=True)


class MaintenanceFromEquipment(BaseModel):
    id: int
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str
    equiptment_id: int

    model_config = ConfigDict(from_attributes=True)


class EditMaintenanceSchema(BaseModel):
    date: date
    observations: Optional[str] = None
    state: Optional[bool] = None
    maintenance_type: str

    model_config = ConfigDict(from_attributes=True)
