from typing import Optional

from pydantic import BaseModel


class StageSchema(BaseModel):
    id: Optional[int] = None
    name: str
    project_id: Optional[int] = None

    class Config:
        from_attributes = True
