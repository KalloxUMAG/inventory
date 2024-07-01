from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Brand
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

class BrandService:
    async def get_brands(self, db: Session):
        return db.query(Brand).all()
    async def get_brand(self, brand_id: int, db: Session):
        return db.query(Brand).filter(Brand.id == brand_id).first()
    async def add_brand(self, brand_name: str, db: Session):
        db_brand = db.query(Brand).filter(func.lower(Brand.name) == brand_name.lower()).first()
        if db_brand:
            return db_brand
        brand = Brand(name=brand_name)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    async def update_brand(self, brand: BasicOptionSchemaWithId, data_update: BasicOptionSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(brand, key, value)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    async def delete_brand(self, brand: BasicOptionSchemaWithId, db: Session):
        db.delete(brand)
        db.commit()