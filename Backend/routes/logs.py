from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services.logs import LogService
from schemas.log_schema import LogSchema

from auth.auth_bearer import JWTBearer

logs = APIRouter(dependencies=[Depends(JWTBearer())], prefix="/api/logs")
service = LogService()


@logs.get("", response_model=List[LogSchema])
async def get_logs(db: Session = Depends(get_db)):
    logs = await service.get_logs(db)
    return logs