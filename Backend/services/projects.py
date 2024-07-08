from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Project
from schemas.basic_option_schema import ProjectSchema, ProjectSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class ProjectService:
    async def get_projects(self, db: Session):
        return db.query(Project).all()
    async def get_project(self, project_id: int, db: Session):
        return db.query(Project).filter(Project.id == project_id).first()
    @log_func_calls("projects", CREATE_LOG)
    async def add_project(self, user_id: int, project: ProjectSchema, db: Session):
        db_project = db.query(Project).filter(func.lower(Project.name) == project.name.lower(), Project.owner_id == project.owner_id).first()
        if db_project:
            return db_project
        project = Project(name=project.name, owner_id=project.owner_id)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    @log_func_calls("projects", UPDATE_LOG)
    async def update_project(self, user_id: int, project: ProjectSchemaWithId, data_update: ProjectSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    @log_func_calls("projects", DELETE_LOG)
    async def delete_project(self, user_id: int, project: ProjectSchemaWithId, db: Session):
        db.delete(project)
        db.commit()
        return project