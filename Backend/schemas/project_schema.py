from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProjectSchema(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True