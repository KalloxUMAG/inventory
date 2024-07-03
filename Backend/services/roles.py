from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Role
from schemas.role_schema import RoleSchema, RoleSchemaWithId

class RoleService:
    async def get_roles(self, db: Session):
        return db.query(Role).all()
    async def get_role(self, role_id: int, db: Session):
        return db.query(Role).filter(Role.id == role_id).first()
    async def add_role(self, role: RoleSchema, db: Session):
        new_role = Role(name=role.name, description=role.description)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role
    async def update_role(self, role: RoleSchemaWithId, data_update: RoleSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(role, key, value)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    async def delete_role(self, role: RoleSchemaWithId, db: Session):
        db.delete(role)
        db.commit()