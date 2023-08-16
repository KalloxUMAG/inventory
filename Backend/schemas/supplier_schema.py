from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplierSchema(BaseModel):
    id: Optional[int] = None
    name: str
    rut: Optional[str] = None
    city_address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
