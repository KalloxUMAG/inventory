from typing import Optional

from pydantic import BaseModel


class SupplierContactSchema(BaseModel):
    id: Optional[int] = None
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    supplier_id: int

    class Config:
        orm_mode = True
