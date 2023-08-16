from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    id: Optional[int] = None
    name: str
    unit_id: int

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
