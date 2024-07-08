from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.project_owners import ProjectOwnerService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

project_owners = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["projects"], prefix="/api/project_owners"
)
service = ProjectOwnerService()


@project_owners.get("", response_model=List[BasicOptionSchemaWithId])
async def get_project_owners(db: Session = Depends(get_db)):
    project_owners = await service.get_project_owners(db)
    return project_owners


@project_owners.post("", status_code=HTTP_201_CREATED)
async def add_project_owner(project_owner: BasicOptionSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    project_owner = await service.add_project_owner(user_id=get_user_id_from_token(dependencies), project_owner_name=project_owner.name, db=db)
    content = str(project_owner.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@project_owners.get("/{project_owner_id}", response_model=BasicOptionSchemaWithId)
async def get_project_owner(project_owner_id: int, db: Session = Depends(get_db)):
    project_owner = await service.get_project_owner(project_owner_id, db)
    if not project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return project_owner


@project_owners.put("/{project_owner_id}", response_model=BasicOptionSchemaWithId)
async def update_project_owner(
    data_update: BasicOptionSchema,
    project_owner_id: int,
    dependencies=Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    project_owner = await service.get_project_owner(project_owner_id, db)
    if not project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    project_owner = await service.update_project_owner(user_id=get_user_id_from_token(dependencies), project_owner=project_owner, data_update=data_update, db=db)
    return project_owner


@project_owners.delete("/{project_owner_id}", status_code=HTTP_200_OK)
async def delete_project_owner(project_owner_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_project_owner = await service.get_project_owner(project_owner_id, db)
    if not db_project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_project_owner(user_id=get_user_id_from_token(dependencies), project_owner=db_project_owner, db=db)
    return Response(status_code=HTTP_200_OK)
