from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Location

class LocationService:
    async def get_locations(self, db: Session):
        return db.query(Location).all()
    async def get_location(self, location_id: int, db: Session):
        return db.query(Location).filter(Location.id == location_id).first()
    async def add_location(self, location_name: str, db: Session):
        db_location = db.query(Location).filter(func.lower(Location.name) == location_name.lower()).first()
        if db_location:
            return db_location
        location = Location(name=location_name)
        db.add(location)
        db.commit()
        db.refresh(location)
        return location