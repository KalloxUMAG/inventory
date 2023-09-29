from typing import Optional

from pydantic import BaseModel


class SuppliesTypesSchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True
