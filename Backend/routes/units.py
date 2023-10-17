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
from models.models import Building, Unit
from schemas.unit_schema import UnitSchema

from auth.auth_bearer import JWTBearer

units = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/units"
)


@units.get("", response_model=List[UnitSchema])
def get_units(db: Session = Depends(get_db)):
    result = db.query(Unit).all()
    return result


@units.post("", status_code=HTTP_201_CREATED)
def add_unit(unit: UnitSchema, db: Session = Depends(get_db)):
    db_building = db.query(Building).filter(Building.id == unit.building_id).first()
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_unit = (
        db.query(Unit)
        .filter(
            func.lower(Unit.name) == unit.name.lower(),
            Unit.building_id == unit.building_id,
        )
        .first()
    )
    if db_unit:
        content = str(db_unit.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_unit = Unit(name=unit.name, building_id=unit.building_id)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    content = str(new_unit.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@units.get("/unit/{unit_id}", response_model=UnitSchema)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    return db.query(Unit).filter(Unit.id == unit_id).first()


@units.get("/{building_id}", response_model=List[UnitSchema])
def get_units_building(building_id: int, db: Session = Depends(get_db)):
    return db.query(Unit).filter(Unit.building_id == building_id).all()


@units.put("/{unit_id}", response_model=UnitSchema)
def update_unit(data_update: UnitSchema, unit_id: int, db: Session = Depends(get_db)):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_unit, key, value)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


@units.delete("/{unit_id}", status_code=HTTP_204_NO_CONTENT)
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_unit)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
