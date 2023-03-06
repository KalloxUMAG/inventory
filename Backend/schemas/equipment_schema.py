from typing import Optional
from pydantic import BaseModel
from datetime import date

class EquipmentSchema(BaseModel):
    id: Optional[int]
    name: str
    serial_number: Optional[str]
    umag_inventory_code: Optional[int]
    reception_date: date
    maintenance_period: Optional[int]
    last_preventive_mainteinance: Optional[date]
    observation: Optional[str]
    supplier_id: Optional[int]
    invoice_id: Optional[int]
    model_id: Optional[int]
    room_id: Optional[int]


    class Config:
        orm_mode = True

class EquipmentFullSchema(BaseModel):
    id: Optional[int]
    name: str
    serial_number: Optional[str]
    umag_inventory_code: Optional[int]
    reception_date: date
    maintenance_period: Optional[int]
    last_preventive_mainteinance: Optional[date]
    observation: Optional[str]
    room_id: Optional[int]
    room_name: Optional[str]
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    invoice_id: Optional[int]
    invoice_number: Optional[int]
    model_id: Optional[int]
    model_model: Optional[str]

    class Config:
        orm_mode = True