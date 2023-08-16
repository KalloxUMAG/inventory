from typing import Optional

from pydantic import BaseModel


class SupplierSchema(BaseModel):
    id: Optional[int] = None
    name: str
    rut: Optional[str] = None
    city_address: Optional[str] = None

    class Config:
        orm_mode = True
