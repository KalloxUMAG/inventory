from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import Stage
from routes.projects import get_project
from schemas.stage_schema import StageSchema

from auth.auth_bearer import JWTBearer

stages = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["projects"], prefix="/api/stages"
)


@stages.get("", response_model=List[StageSchema])
def get_stages(db: Session = Depends(get_db)):
    result = db.query(Stage).all()
    return result


@stages.post("", status_code=HTTP_201_CREATED)
def add_stage(stage: StageSchema, db: Session = Depends(get_db)):
    db_project = get_project(stage.project_id, db=db)
    if not db_project:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_stage = (
        db.query(Stage)
        .filter(
            func.lower(Stage.name) == stage.name.lower(),
            Stage.project_id == stage.project_id,
        )
        .first()
    )
    if db_stage:
        content = str(db_stage.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_stage = Stage(name=stage.name, project_id=stage.project_id)
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    content = str(new_stage.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@stages.get("/stage/{stage_id}", response_model=StageSchema)
def get_stage(stage_id: int, db: Session = Depends(get_db)):
    return db.query(Stage).filter(Stage.id == stage_id).first()


@stages.get("/{project_id}", response_model=List[StageSchema])
def get_stages_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(Stage).filter(Stage.project_id == project_id).all()


@stages.put("/{stage_id}", response_model=StageSchema)
def update_stage(
    data_update: StageSchema, stage_id: int, db: Session = Depends(get_db)
):
    db_stage = get_stage(stage_id, db=db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    if data_update.project_id is not None:
        db_project = get_project(data_update.project_id, db=db)
        if not db_project:
            return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_stage, key, value)
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


@stages.delete("/{stage_id}", status_code=HTTP_204_NO_CONTENT)
def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    db_stage = get_stage(stage_id, db=db)
    if not db_stage:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_stage)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
