from pydantic import BaseModel


class UserGroupRoleSchema(BaseModel):
    user_id: int
    group_id: int
    role_id: int

class UserGroupRoleFullSchema(BaseModel):
    user_id: int
    user_name: str
    group_id: int
    group_name: str
    role_id: int
    role_name: str
    create: bool
    read: bool
    update: bool
    delete: bool

    class Config:
        from_attributes = True
