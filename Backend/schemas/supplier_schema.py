from typing import List, Optional

from pydantic import BaseModel
from schemas.supplier_contact_schema import SupplierContactBasicSchema

class SupplierSchema(BaseModel):
    name: str
    rut: Optional[str] = None
    city_address: Optional[str] = None

    class Config:
        from_attributes = True

class SupplierSchemaWithId(SupplierSchema):
    id: int

    class Config:
        from_attributes = True


class SupplierFullSchema(SupplierSchema):
    contacts: Optional[List[SupplierContactBasicSchema]] = []

    class Config:
        from_attributes = True

class SupplierFullSchemaWithId(SupplierFullSchema):
    id: int

    class Config:
        from_attributes = True