from typing import Optional

from pydantic import BaseModel


class ProjectOwnerSchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True
