from datetime import date
from typing import Optional

from pydantic import BaseModel


class LotSchema(BaseModel):
    id: int
    number: str
    observations: str
    state: Optional[bool] = None
    stock: Optional[int] = None
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    location_id: Optional[int] = None
    location: Optional[str] = None
    sub_location_id: Optional[int] = None
    sub_location: Optional[str] = None

    class Config:
        from_attributes = True


class LotListSchema(BaseModel):
    id: int
    number: str
    reception_date: Optional[date] = None
    due_date: Optional[date] = None
    observations: Optional[str] = None
    state: Optional[bool] = None
    stock: int
    group_id: Optional[int] = None
    group_name: Optional[str] = None
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
        from_attributes = True


class CreateLotSchema(BaseModel):
    number: str
    reception_date: Optional[date] = None
    due_date: Optional[date] = None
    stock: Optional[int] = None
    observations: Optional[str] = None
    state: Optional[bool] = None
    supply_id: int
    group_id: int
    sub_location_id: Optional[int] = None
    project_id: Optional[int] = None
    supplier_id: int

    class Config:
        from_attributes = True
