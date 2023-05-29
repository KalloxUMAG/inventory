from typing import Optional
from pydantic import BaseModel
from datetime import date


class LotListSchema(BaseModel):
    id: int
    number: str
    due_date: Optional[date]
    stock: int
    samples: Optional[int]
    observations: Optional[str]
    supply_name: str
    supply_code: str
    supply_cost: int
    location: Optional[str]
    sub_location: Optional[str]
    project: Optional[str]
    supplier_name: Optional[str]

    class Config:
        orm_mode = True


class CreateLotSchema(BaseModel):
    number: str
    due_date: Optional[date]
    stock: int
    observations: Optional[str]
    supply_id: int
    sub_location_id: Optional[int]
    project_id: Optional[int]

    class Config:
        orm_mode = True
