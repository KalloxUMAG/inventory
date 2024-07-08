from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Role
from schemas.role_schema import RoleSchema, RoleSchemaWithId
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class RoleService:
    async def get_roles(self, db: Session):
        return db.query(Role).all()
    async def get_role(self, role_id: int, db: Session):
        return db.query(Role).filter(Role.id == role_id).first()
    @log_func_calls("roles", CREATE_LOG)
    async def add_role(self, user_id: int, role: RoleSchema, db: Session):
        new_role = Role(name=role.name, description=role.description)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role
    @log_func_calls("roles", UPDATE_LOG)
    async def update_role(self, user_id: int, role: RoleSchemaWithId, data_update: RoleSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(role, key, value)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    @log_func_calls("roles", DELETE_LOG)
    async def delete_role(self, user_id: int, role: RoleSchemaWithId, db: Session):
        db.delete(role)
        db.commit()
        return role