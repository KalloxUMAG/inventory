from datetime import date
from typing import Optional

from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    id: Optional[int] = None
    number: int
    date: date
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True
