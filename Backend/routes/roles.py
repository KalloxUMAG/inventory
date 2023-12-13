from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Role
from schemas.role_schema import RoleSchema

roles = APIRouter(dependencies=[], tags=["roles"], prefix="/api/roless")


@roles.get("", response_model=List[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    result = db.get(Role).all()
    return result


@roles.get("/{role_id}", response_model=RoleSchema)
def get_role(role_id: int, db: Session = Depends(get_db)):
    result = db.get(Role).filter(Role.id == role_id).first()
    return result


@roles.post("", status_code=HTTP_201_CREATED)
def add_role(role: RoleSchema, db: Session = Depends(get_db)):
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    content = str(new_role.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@roles.put("/{role_id}", response_model=RoleSchema)
def update_role(data_update: RoleSchema, role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(role_id, db=db)
    if not db_role:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@roles.delete("/{role_id}", status_code=HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(role_id, db=db)
    if not db_role:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_role)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
