from pydantic import BaseModel


class UserGroupRoleSchema(BaseModel):
    user_id: int
    group_id: int
    role_id: int

    class Config:
        from_attributes = True
