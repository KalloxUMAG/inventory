from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SubLocation
from schemas.basic_option_schema import SubLocationSchema

class SubLocationService:
    async def get_sub_locations(self, db: Session):
        return db.query(SubLocation).all()
    async def get_sub_location_by_location(self, db: Session, location_id: int):
        return db.query(SubLocation).filter(SubLocation.location_id == location_id).all()
    async def add_sub_location(self, db: Session, sub_location: SubLocationSchema):
        db_sub_location = db.query(SubLocation).filter(func.lower(SubLocation.name) == sub_location.name,SubLocation.location_id == sub_location.location_id,).first()
        if db_sub_location:
            return db_sub_location
        new_sub_location = SubLocation(name=sub_location.name, location_id=sub_location.location_id)
        db.add(new_sub_location)
        db.commit()
        db.refresh(new_sub_location)
        return new_sub_location