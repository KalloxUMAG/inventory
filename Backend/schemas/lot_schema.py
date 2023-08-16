from datetime import date
from typing import Optional

from pydantic import BaseModel


class LotListSchema(BaseModel):
    id: int
    number: str
    due_date: Optional[date] = None
    observations: Optional[str] = None
    state: Optional[bool] = None
    location_id: Optional[int] = None
    location: Optional[str] = None
    sub_location_id: Optional[int] = None
    sub_location: Optional[str] = None
    project_id: Optional[int] = None
    project: Optional[str] = None
    project_owner_id: Optional[int] = None
    project_owner_name: Optional[str] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None

    class Config:
        orm_mode = True


class CreateLotSchema(BaseModel):
    number: str
    due_date: Optional[date] = None
    observations: Optional[str] = None
    state: Optional[bool] = None
    supply_id: int
    sub_location_id: Optional[int] = None
    project_id: Optional[int] = None
    supplier_id: int

    class Config:
        orm_mode = True
