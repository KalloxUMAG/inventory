from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import ProjectOwner
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

class ProjectOwnerService:
    async def get_project_owners(self, db: Session):
        return db.query(ProjectOwner).all()
    async def get_project_owner(self, project_owner_id: int, db: Session):
        return db.query(ProjectOwner).filter(ProjectOwner.id == project_owner_id).first()
    async def add_project_owner(self, project_owner_name: str, db: Session):
        db_project_owner = db.query(ProjectOwner).filter(func.lower(ProjectOwner.name) == project_owner_name.lower()).first()
        if db_project_owner:
            return db_project_owner
        project_owner = ProjectOwner(name=project_owner_name)
        db.add(project_owner)
        db.commit()
        db.refresh(project_owner)
        return project_owner
    async def update_project_owner(self, project_owner: BasicOptionSchemaWithId, data_update: BasicOptionSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(project_owner, key, value)
        db.add(project_owner)
        db.commit()
        db.refresh(project_owner)
        return project_owner
    async def delete_project_owner(self, project_owner: BasicOptionSchemaWithId, db: Session):
        db.delete(project_owner)
        db.commit()