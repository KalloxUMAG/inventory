from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SystemRoles, Users, RoleModuleRelation, Modules
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class SystemRolesService:
    async def get_system_roles(self, db: Session, user_id: int):
        user_role = db.query(Users.id, SystemRoles.name).filter(Users.id == user_id, SystemRoles.id == Users.role_id).first()
        return user_role