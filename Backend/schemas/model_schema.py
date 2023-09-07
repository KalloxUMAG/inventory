from typing import Optional

from pydantic import BaseModel


class ModelSchema(BaseModel):
    id: Optional[int] = None
    name: str
    brand_id: int

    class Config:
        from_attributes = True
