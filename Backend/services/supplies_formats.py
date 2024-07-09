from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SupplyFormat
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class SupplyFormatService:
    async def get_supply_formats(self, db: Session):
        return db.query(SupplyFormat).all()
    @log_func_calls("supplies_formats", CREATE_LOG)
    async def add_supply_format(self, user_id: int, db: Session, supply_format_name: str):
        db_supply_format = db.query(SupplyFormat).filter(func.lower(SupplyFormat.name) == supply_format_name.lower()).first()
        if db_supply_format:
            return db_supply_format
        supply_format = SupplyFormat(name=supply_format_name)
        db.add(supply_format)
        db.commit()
        db.refresh(supply_format)
        return supply_format