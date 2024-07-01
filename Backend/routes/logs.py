from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Logs
from schemas.log_schema import LogSchema

from auth.auth_bearer import JWTBearer

logs = APIRouter(dependencies=[Depends(JWTBearer())], prefix="/api/logs")


@logs.get("", response_model=List[LogSchema])
def get_logs(db: Session = Depends(get_db)):
    result = db.query(Logs).all()
    return result

def create_logs(user_id: int, target_id: int, tablename: str, action: str, new_data: dict, db: Session = Depends(get_db)):
    log = Logs(user_id=user_id, target_id=target_id, target_table=tablename, action=action, new_data=new_data)
    db.add(log)
    db.commit()
    db.refresh(log)