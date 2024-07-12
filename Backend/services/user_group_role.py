from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import UserGroupRoleRelation
from schemas.user_group_role import UserGroupRoleSchema
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class UserGroupRoleService:
    async def get_users_groups_roles(self, db: Session):
        return db.query(UserGroupRoleRelation).all()
    async def get_user_groups_and_roles(self, user_id: int, db: Session):
        return db.query(UserGroupRoleRelation).filter(UserGroupRoleRelation.user_id == user_id).all()
    async def add_user_group_role(self, user_group_role: UserGroupRoleSchema, db: Session):
        relation = UserGroupRoleRelation(user_id=user_group_role.user_id, group_id=user_group_role.group_id, role_id=user_group_role.role_id)
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation