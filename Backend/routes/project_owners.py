from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import ProjectOwner
from schemas.project_owner_schema import ProjectOwnerSchema

from auth.auth_bearer import JWTBearer

project_owners = APIRouter(dependencies=[Depends(JWTBearer())], tags=["projects"])


@project_owners.get("/api/project_owners", response_model=List[ProjectOwnerSchema])
def get_project_owners(db: Session = Depends(get_db)):
    result = db.query(ProjectOwner).all()
    return result


@project_owners.post("/api/project_owners", status_code=HTTP_201_CREATED)
def add_project_owner(project_owner: ProjectOwnerSchema, db: Session = Depends(get_db)):
    new_project_owner = ProjectOwner(name=project_owner.name)
    db.add(new_project_owner)
    db.commit()
    db.refresh(new_project_owner)
    content = str(new_project_owner.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@project_owners.get(
    "/api/project_owners/{project_owner_id}", response_model=ProjectOwnerSchema
)
def get_project_owner(project_owner_id: int, db: Session = Depends(get_db)):
    return db.query(ProjectOwner).filter(ProjectOwner.id == project_owner_id).first()


@project_owners.put(
    "/api/project_owners/{project_owner_id}", response_model=ProjectOwnerSchema
)
def update_project_owner(
    data_update: ProjectOwnerSchema,
    project_owner_id: int,
    db: Session = Depends(get_db),
):
    db_project_owner = get_project_owner(project_owner_id, db=db)
    if not db_project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_project_owner, key, value)
    db.add(db_project_owner)
    db.commit()
    db.refresh(db_project_owner)
    return db_project_owner


@project_owners.delete(
    "/api/project_owners/{project_owner_id}", status_code=HTTP_204_NO_CONTENT
)
def delete_project_owner(project_owner_id: int, db: Session = Depends(get_db)):
    db_project_owner = get_project_owner(project_owner_id, db=db)
    if not db_project_owner:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_project_owner)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
