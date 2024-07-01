from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Model
from schemas.basic_option_schema import ModelSchema, ModelSchemaWithId

class ModelService:
    async def get_models(self, db: Session):
        return db.query(Model).all()
    async def get_model(self, model_id: int, db: Session):
        return db.query(Model).filter(Model.id == model_id).first()
    async def get_models_brand(self, brand_id: int, db: Session):
        return db.query(Model).filter(Model.brand_id == brand_id).all()
    async def add_model(self, model: ModelSchema, db: Session):
        db_model = db.query(Model).filter(func.lower(Model.name) == model.name.lower(),Model.brand_id == model.brand_id,).first()
        if db_model:
            return db_model
        model = Model(name=model.name, brand_id=model.brand_id)
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    async def update_model(self, model: ModelSchemaWithId, data_update: ModelSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(model, key, value)
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    async def delete_model(self, model: ModelSchemaWithId, db: Session):
        db.delete(model)
        db.commit()
        return model
        