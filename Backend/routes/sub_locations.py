from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Location, SubLocation
from schemas.sub_location_schema import SubLocationSchema

from auth.auth_bearer import JWTBearer

sub_locations = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/sub_locations"
)


@sub_locations.get("", response_model=List[SubLocationSchema])
def get_sub_locations(db: Session = Depends(get_db)):
    result = db.query(SubLocation).all()
    return result


@sub_locations.post("", status_code=HTTP_201_CREATED)
def add_sub_location(sub_location: SubLocationSchema, db: Session = Depends(get_db)):
    db_location = (
        db.query(Location).filter(Location.id == sub_location.location_id).first()
    )
    if not db_location:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_sub_location = SubLocation(
        name=sub_location.name, location_id=sub_location.location_id
    )
    db.add(new_sub_location)
    db.commit()
    db.refresh(new_sub_location)
    content = str(new_sub_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@sub_locations.get("/{location_id}", response_model=List[SubLocationSchema])
def get_sub_locations_locations(location_id: int, db: Session = Depends(get_db)):
    return db.query(SubLocation).filter(SubLocation.location_id == location_id).all()
