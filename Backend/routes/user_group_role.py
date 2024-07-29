from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from config.database import get_db
from services.user_group_role import UserGroupRoleService
from schemas.user_group_role import UserGroupRoleSchema, UserGroupRoleFullSchema

user_group_role = APIRouter(dependencies=[], tags=["roles"], prefix="/api/user_rol_group")
service = UserGroupRoleService()


@user_group_role.get("")
async def get_users_groups_roles(db: Session = Depends(get_db)):
    roles = await service.get_users_groups_roles(db=db)
    return roles
@user_group_role.get("/{user_id}", response_model=List[UserGroupRoleFullSchema])
async def get_user_groups_and_roles(user_id: int, db: Session = Depends(get_db)):
    roles = await service.get_user_groups_and_roles(user_id=user_id, db=db)
    return roles
@user_group_role.post("")
async def add_user_group_role(user_group_role: UserGroupRoleSchema, db: Session = Depends(get_db)):
    role = await service.add_user_group_role(user_group_role=user_group_role, db=db)
    return Response(status_code=HTTP_201_CREATED)