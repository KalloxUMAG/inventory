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
from models.models import Building
from schemas.building_schema import BuildingSchema

from auth.auth_bearer import JWTBearer

buildings = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/buildings"
)


@buildings.get("", response_model=List[BuildingSchema])
def get_buildings(db: Session = Depends(get_db)):
    result = db.query(Building).all()
    return result


@buildings.post("", status_code=HTTP_201_CREATED)
def add_building(building: BuildingSchema, db: Session = Depends(get_db)):
    db_building = (
        db.query(Building)
        .filter(func.lower(Building.name) == building.name.lower())
        .first()
    )
    if db_building:
        content = str(db_building.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_building = Building(name=building.name)
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    content = str(new_building.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@buildings.get("/{building_id}", response_model=BuildingSchema)
def get_building(building_id: int, db: Session = Depends(get_db)):
    return db.query(Building).filter(Building.id == building_id).first()


@buildings.put("/{building_id}", response_model=BuildingSchema)
def update_building(
    data_update: BuildingSchema, building_id: int, db: Session = Depends(get_db)
):
    db_building = db.query(Building).filter(Building.id == building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_building, key, value)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


@buildings.delete("/{building_id}", status_code=HTTP_204_NO_CONTENT)
def delete_building(building_id: int, db: Session = Depends(get_db)):
    db_building = db.query(Building).filter(Building.id == building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_building)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
