from typing import Optional

from pydantic import BaseModel, ConfigDict


class ModelSchema(BaseModel):
    id: Optional[int] = None
    name: str
    brand_id: int

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
