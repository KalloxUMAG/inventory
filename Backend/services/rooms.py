from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Room
from schemas.basic_option_schema import RoomSchema, RoomSchemaWithId

class RoomService:
    async def get_rooms(self, db: Session):
        return db.query(Room).all()
    async def get_room(self, room_id: int, db: Session):
        return db.query(Room).filter(Room.id == room_id).first()
    async def get_rooms_by_unit(self, unit_id: int, db: Session):
        return db.query(Room).filter(Room.unit_id == unit_id).all()
    async def add_room(self, room: RoomSchema, db: Session):
        db_room = db.query(Room).filter(func.lower(Room.name) == room.name.lower(), Room.unit_id == room.unit_id).first()
        if db_room:
            return db_room
        room = Room(name=room.name, unit_id=room.unit_id)
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    async def update_room(self, room: RoomSchemaWithId, data_update: RoomSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(room, key, value)
        db.commit()
        db.refresh(room)
        return room
    async def delete_room(self, room: RoomSchemaWithId, db: Session):
        db.delete(room)
        db.commit()
        return room