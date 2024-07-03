from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from services.sub_locations import SubLocationService
from services.locations import LocationService
from schemas.basic_option_schema import SubLocationSchema, SubLocationSchemaWithId

from auth.auth_bearer import JWTBearer

sub_locations = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/sub_locations"
)
service = SubLocationService()
location_service = LocationService()


@sub_locations.get("", response_model=List[SubLocationSchemaWithId])
async def get_sub_locations(db: Session = Depends(get_db)):
    sub_locations = await service.get_sub_locations(db)
    return sub_locations


@sub_locations.post("", status_code=HTTP_201_CREATED)
async def add_sub_location(sub_location: SubLocationSchema, db: Session = Depends(get_db)):
    db_location = location_service.get_location(db, sub_location.location_id)
    if not db_location:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_sub_location = await service.add_sub_location(db, sub_location)
    content = str(new_sub_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@sub_locations.get("/{location_id}", response_model=List[SubLocationSchemaWithId])
async def get_sub_locations_locations(location_id: int, db: Session = Depends(get_db)):
    sub_location = await service.get_sub_location_by_location(db, location_id)
    return sub_location
