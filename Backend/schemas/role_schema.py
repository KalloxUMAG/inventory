from typing import Optional

from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GrantRoleSchema(BaseModel):
    user_id: int
    group_id: int
    role_id: int

    class Config:
        from_attributes = True
