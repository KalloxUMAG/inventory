from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from config.database import get_db
from models.models import Location
from schemas.location_schema import LocationSchema

from auth.auth_bearer import JWTBearer

locations = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/locations"
)


@locations.get("", response_model=List[LocationSchema])
def get_locations(db: Session = Depends(get_db)):
    result = db.query(Location).all()
    return result


@locations.post("", status_code=HTTP_201_CREATED)
def add_location(location: LocationSchema, db: Session = Depends(get_db)):
    db_location = (
        db.query(Location)
        .filter(func.lower(Location.name) == location.name.lower())
        .first()
    )
    if db_location:
        content = str(db_location.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_location = Location(name=location.name)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    content = str(new_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@locations.get("/{location_id}", response_model=LocationSchema)
def get_location(location_id: int, db: Session = Depends(get_db)):
    return db.query(Location).filter(Location.id == location_id).first()
