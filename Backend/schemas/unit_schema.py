from typing import Optional

from pydantic import BaseModel, ConfigDict


class UnitSchema(BaseModel):
    id: Optional[int] = None
    name: str
    building_id: int

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
