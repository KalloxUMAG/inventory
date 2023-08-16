from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from models.models import Location
from schemas.location_schema import LocationSchema

locations = APIRouter()


@locations.get("/api/locations", response_model=List[LocationSchema], tags=["locations"])
def get_locations(db: Session = Depends(get_db)):
    result = db.query(Location).all()
    return result


@locations.post("/api/locations", status_code=HTTP_201_CREATED, tags=["locations"])
def add_location(location: LocationSchema, db: Session = Depends(get_db)):
    new_location = Location(name=location.name)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    content = str(new_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@locations.get("/api/locations/{location_id}", response_model=LocationSchema, tags=["locations"])
def get_location(location_id: int, db: Session = Depends(get_db)):
    return db.query(Location).filter(Location.id == location_id).first()
