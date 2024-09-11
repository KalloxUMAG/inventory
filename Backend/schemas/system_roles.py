from typing import List, Optional

from pydantic import BaseModel

class SystemRoleSchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True