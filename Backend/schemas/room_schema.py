from typing import Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: Optional[int] = None
    name: str
    unit_id: int

    class Config:
        orm_mode = True
