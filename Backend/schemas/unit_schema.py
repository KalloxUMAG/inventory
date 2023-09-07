from typing import Optional

from pydantic import BaseModel


class UnitSchema(BaseModel):
    id: Optional[int] = None
    name: str
    building_id: int

    class Config:
        from_attributes = True
