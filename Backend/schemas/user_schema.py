from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.user_group_role import BasicNoUserGroupRoleSchema

class User(BaseModel):
    id: Optional[int]
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disable: Optional[bool] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True


class requestdetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    fullname: str

    class Config:
        from_attributes = True

class UserEdit(BaseModel):
    id: int
    username: str
    email: str
    fullname: str

    class Config:
        from_attributes = True


class requestdetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    fullname: str


class changepassword(BaseModel):
    email: Optional[str] = None
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime


class FilterUser(BaseModel):
    id: Optional[int]
    username: Optional[str] = None
    email: Optional[str] = None
    fullname: Optional[str] = None
    group_roles: List[BasicNoUserGroupRoleSchema]

    class Config:
        from_attributes = True
