from datetime import date
from typing import Optional

from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    number: int
    date: date
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True

class InvoiceSchemaWithId(InvoiceSchema):
    id: int

    class Config:
        from_attributes = True
