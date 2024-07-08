from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.buildings import BuildingService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

buildings = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/buildings"
)
service = BuildingService()


@buildings.get("", response_model=List[BasicOptionSchemaWithId])
async def get_buildings(db: Session = Depends(get_db)):
    buildings = await service.get_builds(db)
    return buildings


@buildings.post("", status_code=HTTP_201_CREATED)
async def add_building(building: BasicOptionSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    building = await service .add_build(user_id=get_user_id_from_token(dependencies), build_name=building.name, db=db)
    content = str(building.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@buildings.get("/{building_id}", response_model=BasicOptionSchemaWithId)
async def get_building(building_id: int, db: Session = Depends(get_db)):
    building = await service.get_build(db, build_id=building_id)
    if not building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return building


@buildings.put("/{building_id}", response_model=BasicOptionSchemaWithId)
async def update_building(
    data_update: BasicOptionSchema, building_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_building = await service.get_build(db, build_id=building_id)
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    building = await service.update_build(user_id=get_user_id_from_token(dependencies), build=db_building, data_update=data_update, db=db)
    return building


@buildings.delete("/{building_id}", status_code=HTTP_200_OK)
async def delete_building(building_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_building = await service.get_build(db, build_id=building_id)
    if not db_building:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_build(user_id=get_user_id_from_token(dependencies), db=db, build=db_building)
    return Response(status_code=HTTP_200_OK)
