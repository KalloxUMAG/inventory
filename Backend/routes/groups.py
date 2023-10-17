from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import Groups
from schemas.group_schema import CreateGroupSchema, GroupSchema

from auth.auth_bearer import JWTBearer

groups = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["groups"], prefix="/api/groups"
)


@groups.get("", response_model=List[GroupSchema])
def get_groups(db: Session = Depends(get_db)):
    result = db.query(Groups.id, Groups.name).all()
    return result


@groups.post("", status_code=HTTP_201_CREATED)
def add_groups(group: CreateGroupSchema, db: Session = Depends(get_db)):
    db_group = (
        db.query(Groups).filter(func.lower(Groups.name) == group.name.lower).first()
    )
    if db_group:
        content = str(db_group.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_group = Groups(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    content = str(new_group.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
