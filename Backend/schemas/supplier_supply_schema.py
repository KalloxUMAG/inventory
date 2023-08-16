from pydantic import BaseModel, ConfigDict


class SupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True


class GetSupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int
    name: str
    rut: str
    city_address: str

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
