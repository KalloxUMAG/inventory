from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from config.database import get_db
from services.roles import RoleService
from schemas.role_schema import RoleSchema, RoleSchemaWithId
from auth.auth_bearer import JWTBearer, get_user_id_from_token

roles = APIRouter(dependencies=[Depends(JWTBearer())], tags=["roles"], prefix="/api/roles")
service = RoleService()


@roles.get("", response_model=List[RoleSchemaWithId])
async def get_roles(db: Session = Depends(get_db)):
    roles = await service.get_roles(db)
    return roles


@roles.get("/{role_id}", response_model=RoleSchemaWithId)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    role = await service.get_role(role_id, db)
    if not role:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return role


@roles.post("", status_code=HTTP_201_CREATED)
async def add_role(role: RoleSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    new_role = await service.add_role(user_id=get_user_id_from_token(dependencies), role=role, db=db)
    content = str(new_role.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@roles.put("/{role_id}", response_model=RoleSchemaWithId)
async def update_role(data_update: RoleSchema, role_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_role = await service.get_role(role_id, db)
    if not db_role:
        return Response(status_code=HTTP_404_NOT_FOUND)
    role = await service.update_role(user_id=get_user_id_from_token(dependencies), role=db_role, data_update=data_update, db=db)
    return role


@roles.delete("/{role_id}", status_code=HTTP_200_OK)
async def delete_role(role_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_role = await service.get_role(role_id, db)
    if not db_role:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_role(user_id=get_user_id_from_token(dependencies), role=db_role, db=db)
    return Response(status_code=HTTP_200_OK)
