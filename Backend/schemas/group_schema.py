from typing import Optional

from pydantic import BaseModel


class GroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CreateGroupSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
