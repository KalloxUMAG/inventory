from typing import Optional

from pydantic import BaseModel


class ModelNumberSchema(BaseModel):
    id: Optional[int] = None
    number: str
    model_id: int

    class Config:
        orm_mode = True
