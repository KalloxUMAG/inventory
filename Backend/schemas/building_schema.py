from typing import Optional

from pydantic import BaseModel, ConfigDict


class BuildingSchema(BaseModel):
    id: Optional[int] = None
    name: str

    model_config = ConfigDict(from_attributes=True)
