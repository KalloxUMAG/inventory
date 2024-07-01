from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from services.locations import LocationService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer

locations = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/locations"
)
service = LocationService()


@locations.get("", response_model=List[BasicOptionSchemaWithId])
async def get_locations(db: Session = Depends(get_db)):
    locations = await service.get_locations(db)
    return locations


@locations.post("", status_code=HTTP_201_CREATED)
async def add_location(location: BasicOptionSchema, db: Session = Depends(get_db)):
    location = await service.add_location(location.name, db)
    content = str(location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@locations.get("/{location_id}", response_model=BasicOptionSchemaWithId)
async def get_location(location_id: int, db: Session = Depends(get_db)):
    location = await service.get_location(location_id, db)
    if not location:
        return Response(status_code=404)
    return location
