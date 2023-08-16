from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjectSchema(BaseModel):
    id: Optional[int] = None
    name: str
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
