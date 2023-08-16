from typing import Optional

from pydantic import BaseModel, ConfigDict


class BrandSchema(BaseModel):
    id: Optional[int] = None
    name: str

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
