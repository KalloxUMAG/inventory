from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Unit
from schemas.basic_option_schema import UnitSchema, UnitSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class UnitService:
    async def get_units(self, db: Session):
        return db.query(Unit).all()
    async def get_unit(self, unit_id: int, db: Session):
        return db.query(Unit).filter(Unit.id == unit_id).first()
    async def get_units_by_building(self, building_id: int, db: Session):
        return db.query(Unit).filter(Unit.building_id == building_id).all()
    @log_func_calls("units", CREATE_LOG)
    async def add_unit(self, user_id: int, unit: UnitSchema, db: Session):
        db_unit = db.query(Unit).filter(func.lower(Unit.name) == unit.name.lower(), Unit.building_id == unit.building_id).first()
        if db_unit:
            return db_unit
        unit = Unit(name=unit.name, building_id=unit.building_id)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    @log_func_calls("units", UPDATE_LOG)
    async def update_unit(self, user_id: int, unit: UnitSchemaWithId, data_update: UnitSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(unit, key, value)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    @log_func_calls("units", DELETE_LOG)
    async def delete_unit(self, user_id: int, unit: UnitSchemaWithId, db: Session):
        db.delete(unit)
        db.commit()
        return unit