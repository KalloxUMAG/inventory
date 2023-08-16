from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubLocationSchema(BaseModel):
    id: Optional[int] = None
    name: str
    location_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
