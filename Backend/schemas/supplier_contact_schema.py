from typing import Optional

from pydantic import BaseModel


class SupplierContactSchema(BaseModel):
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    supplier_id: int

    class Config:
        from_attributes = True


class SupplierContactSchemaWithId(SupplierContactSchema):
    id: int

    class Config:
        from_attributes = True


class SupplierContactBasicSchema(BaseModel):
    id: Optional[int] = None
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True