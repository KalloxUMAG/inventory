from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.rooms import RoomService
from services.units import UnitService
from schemas.basic_option_schema import RoomSchema, RoomSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

rooms = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["locations"], prefix="/api/rooms"
)
service = RoomService()
unit_service = UnitService()


@rooms.get("", response_model=List[RoomSchemaWithId])
async def get_rooms(db: Session = Depends(get_db)):
    rooms = await service.get_rooms(db)
    return rooms


@rooms.post("", status_code=HTTP_201_CREATED)
async def add_room(room: RoomSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_unit = await unit_service.get_unit(room.unit_id, db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    room = await service.add_room(user_id=get_user_id_from_token(dependencies), room=room, db=db)
    content = str(room.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@rooms.get("/room/{room_id}", response_model=RoomSchemaWithId)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    room = await service.get_room(room_id, db)
    return room


@rooms.get("/{unit_id}", response_model=List[RoomSchemaWithId])
async def get_rooms_unit(unit_id: int, db: Session = Depends(get_db)):
    rooms = await service.get_rooms_by_unit(unit_id, db)
    return rooms


@rooms.put("/{room_id}", response_model=RoomSchemaWithId)
async def update_room(data_update: RoomSchema, room_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_room = await service.get_room(room_id, db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_unit = await unit_service.get_unit(data_update.unit_id, db)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    room = await service.update_room(user_id=get_user_id_from_token(dependencies), room=db_room, data_update=data_update, db=db)
    return room


@rooms.delete("/{room_id}", status_code=HTTP_200_OK)
async def delete_room(room_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_room = await service.get_room(room_id, db)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete(user_id=get_user_id_from_token(dependencies), room=db_room, db=db)
    db.commit()
    return Response(status_code=HTTP_200_OK)
