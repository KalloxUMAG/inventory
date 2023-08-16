from typing import Optional

from pydantic import BaseModel


class SubLocationSchema(BaseModel):
    id: Optional[int] = None
    name: str
    location_id: Optional[int] = None

    class Config:
        orm_mode = True
