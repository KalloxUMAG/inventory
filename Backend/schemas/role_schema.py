from typing import Optional

from pydantic import BaseModel


class RoleSchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class RoleSchemaWithId(BaseModel):
    id: int
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
