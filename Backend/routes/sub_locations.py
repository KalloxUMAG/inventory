from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Location, SubLocation
from schemas.sub_location_schema import SubLocationSchema

sub_locations = APIRouter()


@sub_locations.get("/api/sub_locations", response_model=List[SubLocationSchema], tags=["locations"])
def get_sub_locations(db: Session = Depends(get_db)):
    result = db.query(SubLocation).all()
    return result


@sub_locations.post("/api/sub_locations", status_code=HTTP_201_CREATED, tags=["locations"])
def add_sub_location(sub_location: SubLocationSchema, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == sub_location.location_id).first()
    if not db_location:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_sub_location = SubLocation(name=sub_location.name, location_id=sub_location.location_id)
    db.add(new_sub_location)
    db.commit()
    db.refresh(new_sub_location)
    content = str(new_sub_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@sub_locations.get(
    "/api/sub_locations/{location_id}", response_model=List[SubLocationSchema], tags=["locations"]
)
def get_sub_locations_locations(location_id: int, db: Session = Depends(get_db)):
    return db.query(SubLocation).filter(SubLocation.location_id == location_id).all()
