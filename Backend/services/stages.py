from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Stage
from schemas.basic_option_schema import StageSchema, StageSchemaWithId

class StageService:
    async def get_stages(self, db: Session):
        stages = db.query(Stage).all()
        return stages
    async def get_stage(self, stage_id: int, db: Session):
        stage = db.query(Stage).filter(Stage.id == stage_id).first()
        return stage
    async def get_stages_by_project(self, project_id: int, db: Session):
        stages = db.query(Stage).filter(Stage.project_id == project_id).all()
        return stages
    async def add_stage(self, stage: StageSchema, db: Session):
        db_stage = db.query(Stage).filter(func.lower(Stage.name) == stage.name.lower(),Stage.project_id == stage.project_id).first()
        if db_stage:
            return db_stage
        new_stage = Stage(name=stage.name, project_id=stage.project_id)
        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)
        return new_stage
    async def update_stage(self, stage: StageSchemaWithId, data_update: StageSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(stage, key, value)
        db.add(stage)
        db.commit()
        db.refresh(stage)
        return stage
    async def delete_stage(self, stage: StageSchemaWithId, db: Session):
        db.delete(stage)
        db.commit()