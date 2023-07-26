from typing import Optional
from pydantic import BaseModel
from datetime import date


class LotListSchema(BaseModel):
    id: int
    number: str
    due_date: Optional[date]
    observations: Optional[str]
    state: Optional[bool]
    location_id: Optional[int]
    location: Optional[str]
    sub_location_id: Optional[int]
    sub_location: Optional[str]
    project_id: Optional[int]
    project: Optional[str]
    project_owner_id: Optional[int]
    project_owner_name: Optional[str]
    supplier_id: Optional[int]
    supplier_name: Optional[str]

    class Config:
        orm_mode = True


class CreateLotSchema(BaseModel):
    number: str
    due_date: Optional[date]
    observations: Optional[str]
    state: Optional[bool]
    supply_id: int
    sub_location_id: Optional[int]
    project_id: Optional[int]
    supplier_id: int

    class Config:
        orm_mode = True
