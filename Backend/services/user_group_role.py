from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import UserGroupRoleRelation, Users, Groups, Role
from schemas.user_group_role import UserGroupRoleSchema
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class UserGroupRoleService:
    async def get_users_groups_roles(self, db: Session):
        return db.query(UserGroupRoleRelation).all()
    async def get_user_groups_and_roles(self, user_id: int, db: Session):
        result = db.query(Users.id.label("user_id"), Users.fullname.label("user_name"), Groups.id.label("group_id"), Groups.name.label("group_name"), Role.id.label("role_id"), Role.name.label("role_name"), Role.create, Role.read, Role.update, Role.delete).filter(Users.id == user_id).outerjoin(UserGroupRoleRelation, UserGroupRoleRelation.user_id == Users.id).outerjoin(Groups, Groups.id == UserGroupRoleRelation.group_id).outerjoin(Role, Role.id == UserGroupRoleRelation.role_id).all()
        return result
    async def get_user_group_roles(self, user_id: int, group_id: int, db: Session):
        result = db.query(UserGroupRoleRelation.user_id, Role.id.label("role_id"), Role.name.label("role_name"), Role.create, Role.read, Role.update, Role.delete).outerjoin(Role, Role.id == UserGroupRoleRelation.role_id).filter(UserGroupRoleRelation.user_id == user_id, UserGroupRoleRelation.group_id == group_id).first()
        return result
    async def get_group_users_and_roles(self, group_id: int, db: Session):
        result = db.query(Users.id.label("user_id"), Users.fullname, Users.email, Users.username, Users.disable, Groups.id.label("group_id"), Role.id.label("role_id"), Role.name.label("role_name")).filter(Groups.id == group_id).outerjoin(UserGroupRoleRelation, UserGroupRoleRelation.group_id == Groups.id).outerjoin(Users, Users.id == UserGroupRoleRelation.user_id).outerjoin(Role, Role.id == UserGroupRoleRelation.role_id).all()
        return result
    async def add_user_group_role(self, user_group_role: UserGroupRoleSchema, db: Session):
        relation = UserGroupRoleRelation(user_id=user_group_role.user_id, group_id=user_group_role.group_id, role_id=user_group_role.role_id)
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation
    async def delete_user_group_role(self, user_id: int, group_id: int, db: Session):
        db.query(UserGroupRoleRelation).filter(UserGroupRoleRelation.user_id == user_id, UserGroupRoleRelation.group_id == group_id).delete()
        db.commit()
        return True