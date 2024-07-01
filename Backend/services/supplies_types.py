from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SupplyType

class SupplyTypeService:
    async def get_supply_types(self, db: Session):
        return db.query(SupplyType).all()
    async def add_supply_type(self, db: Session, supply_type_name: str):
        db_supply_type = db.query(SupplyType).filter(func.lower(SupplyType.name) == supply_type_name.lower()).first()
        if db_supply_type:
            return db_supply_type
        supply_type = SupplyType(name=supply_type_name)
        db.add(supply_type)
        db.commit()
        return supply_type