from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.units import UnitService
from services.buildings import BuildingService
from schemas.basic_option_schema import UnitSchema, UnitSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

units = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/units"
)
service = UnitService()
building_service = BuildingService()


@units.get("", response_model=List[UnitSchemaWithId])
async def get_units(db: Session = Depends(get_db)):
    units = await service.get_units(db)
    return units


@units.post("", status_code=HTTP_201_CREATED)
async def add_unit(unit: UnitSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_building = await building_service.get_build(build_id=unit.building_id, db=db)
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND, content="Building not found")
    unit = await service.add_unit(user_id=get_user_id_from_token(dependencies), unit=unit, db=db)
    content = str(unit.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@units.get("/unit/{unit_id}", response_model=UnitSchemaWithId)
async def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = await service.get_unit(unit_id, db)
    if not unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return unit


@units.get("/{building_id}", response_model=List[UnitSchemaWithId])
async def get_units_building(building_id: int, db: Session = Depends(get_db)):
    units = await service.get_units_by_building(building_id, db)
    return units


@units.put("/{unit_id}", response_model=UnitSchemaWithId)
async def update_unit(data_update: UnitSchema, unit_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_unit = await service.get_unit(unit_id, db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    unit = await service.update_unit(user_id=get_user_id_from_token(dependencies), unit=db_unit, data_update=data_update, db=db)
    return unit


@units.delete("/{unit_id}", status_code=HTTP_200_OK)
async def delete_unit(unit_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_unit = await service.get_unit(unit_id, db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_unit(user_id=get_user_id_from_token(dependencies), unit=db_unit, db=db)
    return Response(status_code=HTTP_200_OK)
