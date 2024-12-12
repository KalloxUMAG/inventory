from pydantic import BaseModel
from typing import Optional

class SupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: Optional[int] = None

    class Config:
        from_attributes = True


class GetSupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: Optional[int] = None
    name: str
    rut: str
    city_address: str

    class Config:
        from_attributes = True
