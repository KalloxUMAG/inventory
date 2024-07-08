from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Room
from schemas.basic_option_schema import RoomSchema, RoomSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class RoomService:
    async def get_rooms(self, db: Session):
        return db.query(Room).all()
    async def get_room(self, room_id: int, db: Session):
        return db.query(Room).filter(Room.id == room_id).first()
    async def get_rooms_by_unit(self, unit_id: int, db: Session):
        return db.query(Room).filter(Room.unit_id == unit_id).all()
    @log_func_calls("rooms", CREATE_LOG)
    async def add_room(self, user_id: int, room: RoomSchema, db: Session):
        db_room = db.query(Room).filter(func.lower(Room.name) == room.name.lower(), Room.unit_id == room.unit_id).first()
        if db_room:
            return db_room
        room = Room(name=room.name, unit_id=room.unit_id)
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    @log_func_calls("rooms", UPDATE_LOG)
    async def update_room(self, user_id: int, room: RoomSchemaWithId, data_update: RoomSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(room, key, value)
        db.commit()
        db.refresh(room)
        return room
    @log_func_calls("rooms", DELETE_LOG)
    async def delete_room(self, user_id: int, room: RoomSchemaWithId, db: Session):
        db.delete(room)
        db.commit()
        return room