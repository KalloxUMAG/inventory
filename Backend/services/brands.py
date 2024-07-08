from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Brand
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class BrandService:
    async def get_brands(self, db: Session):
        return db.query(Brand).all()
    async def get_brand(self, brand_id: int, db: Session):
        return db.query(Brand).filter(Brand.id == brand_id).first()
    @log_func_calls("brands", CREATE_LOG)
    async def add_brand(self, user_id: int, brand_name: str, db: Session):
        db_brand = db.query(Brand).filter(func.lower(Brand.name) == brand_name.lower()).first()
        if db_brand:
            return db_brand
        brand = Brand(name=brand_name)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    @log_func_calls("brands", UPDATE_LOG)
    async def update_brand(self, user_id: int, brand: BasicOptionSchemaWithId, data_update: BasicOptionSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(brand, key, value)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    @log_func_calls("brands", DELETE_LOG)
    async def delete_brand(self, user_id: int, brand: BasicOptionSchemaWithId, db: Session):
        db.delete(brand)
        db.commit()
        return brand