from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Unit
from schemas.basic_option_schema import UnitSchema, UnitSchemaWithId

class UnitService:
    async def get_units(self, db: Session):
        return db.query(Unit).all()
    async def get_unit(self, unit_id: int, db: Session):
        print("unit_id", unit_id)
        return db.query(Unit).filter(Unit.id == unit_id).first()
    async def get_units_by_building(self, building_id: int, db: Session):
        return db.query(Unit).filter(Unit.building_id == building_id).all()
    async def add_unit(self, unit: UnitSchema, db: Session):
        db_unit = db.query(Unit).filter(func.lower(Unit.name) == unit.name.lower(), Unit.building_id == unit.building_id).first()
        if db_unit:
            return db_unit
        unit = Unit(name=unit.name, building_id=unit.building_id)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    async def update_unit(self, unit: UnitSchemaWithId, data_update: UnitSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(unit, key, value)
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    async def delete_unit(self, unit: UnitSchemaWithId, db: Session):
        db.delete(unit)
        db.commit()
        return unit