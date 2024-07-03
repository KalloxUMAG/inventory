from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import ModelNumber
from schemas.basic_option_schema import ModelNumberSchema, ModelNumberSchemaWithId

class ModelNumberService:
    async def get_model_numbers(self, db: Session):
        print(db)
        return db.query(ModelNumber).all()
    async def get_model_number(self, model_number_id: int, db: Session):
        return db.query(ModelNumber).filter(ModelNumber.id == model_number_id).first()
    async def get_model_number_by_model(self, model_id: int, db: Session):
        return db.query(ModelNumber).filter(ModelNumber.model_id == model_id).all()
    async def add_model_number(self, model_number: ModelNumberSchema, db: Session):
        db_model_number = db.query(ModelNumber).filter(func.lower(ModelNumber.number) == model_number.number.lower(),ModelNumber.model_id == model_number.model_id).first()
        if db_model_number:
            return db_model_number
        new_model_number = ModelNumber(
            number=model_number.number, model_id=model_number.model_id
        )
        db.add(new_model_number)
        db.commit()
        db.refresh(new_model_number)
        return new_model_number
    async def update_model_number(self, model_number: ModelNumberSchemaWithId, data_update: ModelNumberSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(model_number, key, value)
        db.add(model_number)
        db.commit()
        db.refresh(model_number)
        return model_number
    async def delete_model_number(self, model_number: ModelNumberSchemaWithId, db: Session):
        db.delete(model_number)
        db.commit()
        return model_number