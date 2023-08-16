from typing import Optional

from pydantic import BaseModel, ConfigDict


class ModelNumberSchema(BaseModel):
    id: Optional[int] = None
    number: str
    model_id: int

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
