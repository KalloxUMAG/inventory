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
from models.models import Room
from routes.units import get_unit
from schemas.room_schema import RoomSchema

from auth.auth_bearer import JWTBearer

rooms = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/rooms"
)


@rooms.get("", response_model=List[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    result = db.query(Room).all()
    return result


@rooms.post("", status_code=HTTP_201_CREATED)
def add_room(room: RoomSchema, db: Session = Depends(get_db)):
    db_unit = get_unit(room.unit_id, db=db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_room = (
        db.query(Room)
        .filter(
            func.lower(Room.name) == room.name.lower(), Room.unit_id == room.unit_id
        )
        .first()
    )
    if db_room:
        content = str(db_room.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_room = Room(name=room.name, unit_id=room.unit_id)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    content = str(new_room.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@rooms.get("/room/{room_id}", response_model=RoomSchema)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.id == room_id).first()


@rooms.get("/{unit_id}", response_model=List[RoomSchema])
def get_rooms_unit(unit_id: int, db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.unit_id == unit_id).all()


@rooms.put("/{room_id}", response_model=RoomSchema)
def update_room(data_update: RoomSchema, room_id: int, db: Session = Depends(get_db)):
    db_room = get_room(room_id, db=db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@rooms.delete("/{room_id}", status_code=HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = get_room(room_id, db=db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_room)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
