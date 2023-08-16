from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InvoiceSchema(BaseModel):
    id: Optional[int] = None
    number: int
    date: date
    supplier_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True