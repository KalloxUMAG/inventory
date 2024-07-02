from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Project
from schemas.basic_option_schema import ProjectSchema, ProjectSchemaWithId

class ProjectService:
    async def get_projects(self, db: Session):
        return db.query(Project).all()
    async def get_project(self, project_id: int, db: Session):
        return db.query(Project).filter(Project.id == project_id).first()
    async def add_project(self, project: ProjectSchema, db: Session):
        db_project = db.query(Project).filter(func.lower(Project.name) == project.name.lower(), Project.owner_id == project.owner_id).first()
        if db_project:
            return db_project
        project = Project(name=project.name, owner_id=project.owner_id)
        db.add(project)
        db.commit()
        db.refresh(project)
        return
    async def update_project(self, project: ProjectSchemaWithId, data_update: ProjectSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    async def delete_project(self, project: ProjectSchemaWithId, db: Session):
        db.delete(project)
        db.commit()
        return