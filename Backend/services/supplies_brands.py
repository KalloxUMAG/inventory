from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SupplyBrand

class SupplyBrandService:
    async def get_supply_brands(self, db: Session):
        return db.query(SupplyBrand).all()
    async def add_supply_brand(self, db: Session, supply_brand_name: str):
        db_supply_brand = db.query(SupplyBrand).filter(func.lower(SupplyBrand.name) == supply_brand_name.lower()).first()
        if db_supply_brand:
            return db_supply_brand
        supply_brand = SupplyBrand(name=supply_brand_name)
        db.add(supply_brand)
        db.commit()
        db.refresh(supply_brand)
        return supply_brand