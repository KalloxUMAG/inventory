from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.projects import ProjectService
from services.project_owners import ProjectOwnerService
from schemas.basic_option_schema import ProjectSchema, ProjectSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

projects = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["projects"], prefix="/api/projects"
)
service = ProjectService()
project_owner_service = ProjectOwnerService()


@projects.get("", response_model=List[ProjectSchemaWithId])
async def get_projects(db: Session = Depends(get_db)):
    projects = await service.get_projects(db)
    return projects


@projects.post("", status_code=HTTP_201_CREATED)
async def add_project(project: ProjectSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_project_owner = await project_owner_service.get_project_owner(project.owner_id, db)
    if not db_project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_project = await service.add_project(user_id=get_user_id_from_token(dependencies), project=project, db=db)
    content = str(new_project.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@projects.get("/{project_id}", response_model=ProjectSchemaWithId)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = await service.get_project(project_id, db)
    if not project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return project


@projects.put("/{project_id}", response_model=ProjectSchemaWithId)
async def update_project(
    data_update: ProjectSchema, project_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_project = await get_project(project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if data_update.owner_id:
        db_project_owner = await project_owner_service.get_project_owner(data_update.owner_id, db)
        if not db_project_owner:
            return Response(status_code=HTTP_404_NOT_FOUND)
    project = await service.update_project(user_id=get_user_id_from_token(dependencies), project=db_project, data_update=data_update, db=db)
    return project


@projects.delete("/{project_id}", status_code=HTTP_200_OK)
async def delete_project(project_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_project = await service.get_project(project_id, db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_project(user_id=get_user_id_from_token(dependencies), project=db_project, db=db)
    return Response(status_code=HTTP_200_OK)
