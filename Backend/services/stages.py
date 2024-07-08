from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Stage
from schemas.basic_option_schema import StageSchema, StageSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

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
    @log_func_calls("stages", CREATE_LOG)
    async def add_stage(self, user_id: int, stage: StageSchema, db: Session):
        db_stage = db.query(Stage).filter(func.lower(Stage.name) == stage.name.lower(),Stage.project_id == stage.project_id).first()
        if db_stage:
            return db_stage
        new_stage = Stage(name=stage.name, project_id=stage.project_id)
        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)
        return new_stage
    @log_func_calls("stages", UPDATE_LOG)
    async def update_stage(self, user_id: int, stage: StageSchemaWithId, data_update: StageSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(stage, key, value)
        db.add(stage)
        db.commit()
        db.refresh(stage)
        return stage
    @log_func_calls("stages", DELETE_LOG)
    async def delete_stage(self, user_id: int, stage: StageSchemaWithId, db: Session):
        db.delete(stage)
        db.commit()
        return stage