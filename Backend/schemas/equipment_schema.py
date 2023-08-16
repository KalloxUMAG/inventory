from datetime import date
from typing import Optional

from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    id: Optional[int] = None
    name: str
    serial_number: Optional[str] = None
    umag_inventory_code: Optional[str] = None
    reception_date: Optional[date] = None
    maintenance_period: Optional[int] = None
    last_preventive_mainteinance: Optional[date] = None
    observation: Optional[str] = None
    supplier_id: Optional[int] = None
    invoice_id: Optional[int] = None
    model_number_id: Optional[int] = None
    room_id: Optional[int] = None
    stage_id: Optional[int] = None

    class Config:
        orm_mode = True


class EquipmentListSchema(BaseModel):
    id: Optional[int] = None
    name: str
    serial_number: Optional[str] = None
    umag_inventory_code: Optional[str] = None
    reception_date: Optional[date] = None
    maintenance_period: Optional[int] = None
    last_preventive_mainteinance: Optional[date] = None
    observation: Optional[str] = None
    room_id: Optional[int] = None
    room_name: Optional[str] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None
    invoice_id: Optional[int] = None
    invoice_number: Optional[int] = None
    model_number_id: Optional[int] = None
    model_number: Optional[str] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    stage_id: Optional[int] = None
    stage_name: Optional[str] = None

    class Config:
        orm_mode = True


class EquipmentFullSchema(BaseModel):
    id: Optional[int] = None
    name: str
    serial_number: Optional[str] = None
    umag_inventory_code: Optional[str] = None
    reception_date: Optional[date] = None
    maintenance_period: Optional[int] = None
    observation: Optional[str] = None
    last_preventive_mainteinance: Optional[date] = None
    room_id: Optional[int] = None
    room_name: Optional[str] = None
    unit_id: Optional[int] = None
    unit_name: Optional[str] = None
    building_id: Optional[int] = None
    building_name: Optional[str] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None
    invoice_id: Optional[int] = None
    invoice_number: Optional[int] = None
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    model_number_id: Optional[int] = None
    model_number: Optional[str] = None
    stage_id: Optional[int] = None
    stage_name: Optional[str] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    project_owner_id: Optional[str] = None
    project_owner_name: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateEquipmentSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    serial_number: Optional[str] = None
    umag_inventory_code: Optional[str] = None
    reception_date: Optional[date] = None
    maintenance_period: Optional[int] = None
    last_preventive_mainteinance: Optional[date] = None
    observation: Optional[str] = None
    supplier_id: Optional[int] = None
    invoice_id: Optional[int] = None
    model_number_id: Optional[int] = None
    room_id: Optional[int] = None
    stage_id: Optional[int] = None

    class Config:
        orm_mode = True


class NextMaintenanceSchema(BaseModel):
    id: Optional[int] = None
    maintenance_id: Optional[int] = None
    date: Optional[date] = None

    class Config:
        orm_mode = True
