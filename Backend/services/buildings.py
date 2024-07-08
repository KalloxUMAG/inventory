from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Building
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class BuildingService:
    async def get_builds(self, db: Session):
        return db.query(Building).all()
    async def get_build(self, db: Session, build_id: int):
        return db.query(Building).filter(Building.id == build_id).first()
    @log_func_calls("buildings", CREATE_LOG)
    async def add_build(self, user_id: int, db: Session, build_name: str):
        db_building = (
            db.query(Building).filter(func.lower(Building.name) == build_name.lower()).first()
        )
        if db_building:
            return db_building
        new_building = Building(name=build_name)
        db.add(new_building)
        db.commit()
        db.refresh(new_building)
        return new_building
    @log_func_calls("brands", UPDATE_LOG)
    async def update_build(self, user_id: int, db: Session, build: BasicOptionSchemaWithId, data_update: BasicOptionSchema):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(build, key, value)
        db.add(build)
        db.commit()
        db.refresh(build)
        return build
    @log_func_calls("brands", DELETE_LOG)
    async def delete_build(self, user_id: int, db: Session, build: BasicOptionSchemaWithId):
        db.delete(build)
        db.commit()
        return build