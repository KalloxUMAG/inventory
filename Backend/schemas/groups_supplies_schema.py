from typing import Optional

from pydantic import BaseModel


class GroupSupplySchema(BaseModel):
    group_id: int
    supply_id: int
    quantity: int

    class Config:
        from_attributes = True
