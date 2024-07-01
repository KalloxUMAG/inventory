from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SupplyFormat

class SupplyFormatService:
    async def get_supply_formats(self, db: Session):
        return db.query(SupplyFormat).all()
    async def add_supply_format(self, db: Session, supply_format_name: str):
        db_supply_format = db.query(SupplyFormat).filter(func.lower(SupplyFormat.name) == supply_format_name.lower()).first()
        if db_supply_format:
            return db_supply_format
        supply_format = SupplyFormat(name=supply_format_name)
        db.add(supply_format)
        db.commit()
        db.refresh(supply_format)
        return supply_format