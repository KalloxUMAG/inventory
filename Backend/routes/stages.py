from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.stages import StageService
from services.projects import ProjectService
from schemas.basic_option_schema import StageSchema, StageSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

stages = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["projects"], prefix="/api/stages"
)
service = StageService()
project_service = ProjectService()


@stages.get("", response_model=List[StageSchemaWithId])
async def get_stages(db: Session = Depends(get_db)):
    stages = await service.get_stages(db)
    return stages


@stages.post("", status_code=HTTP_201_CREATED)
async def add_stage(stage: StageSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_project = await project_service.get_project(stage.project_id, db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_stage = await service.add_stage(user_id=get_user_id_from_token(dependencies), stage=stage, db=db)
    content = str(new_stage.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@stages.get("/stage/{stage_id}", response_model=StageSchemaWithId)
async def get_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = await service.get_stage(stage_id, db)
    if not stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return stage


@stages.get("/{project_id}", response_model=List[StageSchemaWithId])
async def get_stages_project(project_id: int, db: Session = Depends(get_db)):
    stages = await service.get_stages_by_project(project_id, db)
    return stages


@stages.put("/{stage_id}", response_model=StageSchemaWithId)
async def update_stage(
    data_update: StageSchema, stage_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_stage = await service.get_stage(stage_id, db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if data_update.project_id is not None:
        db_project = await project_service.get_project(data_update.project_id, db)
        if not db_project:
            return Response(status_code=HTTP_404_NOT_FOUND)
    stage = await service.update_stage(user_id=get_user_id_from_token(dependencies), stage=db_stage, data_update=data_update, db=db)
    return stage


@stages.delete("/{stage_id}", status_code=HTTP_200_OK)
async def delete_stage(stage_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_stage = await service.get_stage(stage_id, db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_stage(user_id=get_user_id_from_token(dependencies), stage=db_stage, db=db)
    return Response(status_code=HTTP_200_OK)
