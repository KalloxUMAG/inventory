from typing import Optional

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: Optional[int] = None
    name: str
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True
