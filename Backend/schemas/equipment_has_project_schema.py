from pydantic import BaseModel
from typing import Optional

class EquipmentHasProjectSchema(BaseModel):
    equipment_id: int
    project_id: int
    stage_id: Optional[int]

    class Config:
        orm_mode = True

class EquipmentHasProjectsSchema(BaseModel):
    project_id: int
    stage_id: Optional[int]

    class Config:
        orm_mode = True

class ProjectHasEquipmentsSchema(BaseModel):
    equipment_id: int
    stage_id: Optional[int]

    class Config:
        orm_mode = True