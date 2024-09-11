from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from config.database import get_db

from auth.auth_bearer import JWTBearer, get_user_id_from_token

from services.system_roles import SystemRolesService

system_roles = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["system_roles"], prefix="/api/modules"
)

systemRolesService = SystemRolesService()

@system_roles.get("")
async def get_system_roles(db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
   user_id = get_user_id_from_token(dependencies)
   response = await systemRolesService.get_system_roles(db, user_id)
   return response