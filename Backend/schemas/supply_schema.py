from typing import Optional
from pydantic import BaseModel
from datetime import date


class SupplyListSchema(BaseModel):
    id: int
    code: str
    number: str

    class Config:
        orm_mode = True
