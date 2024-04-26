from typing import List, Optional, Any

from pydantic import BaseModel

class GroupSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    other_names: Optional[List[str]] = None

    class Config:
        from_attributes = True


class CreateGroupSchema(BaseModel):
    name: str
    description: Optional[str] = None
    other_names: Optional[List[str]] = None

    class Config:
        from_attributes = True
