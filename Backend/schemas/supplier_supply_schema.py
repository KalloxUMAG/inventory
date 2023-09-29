from pydantic import BaseModel


class SupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int

    class Config:
        from_attributes = True


class GetSupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int
    name: str
    rut: str
    city_address: str

    class Config:
        from_attributes = True
