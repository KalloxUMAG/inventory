from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Logs
from schemas.log_schema import LogSchema

class LogService:
    async def get_logs(self, db: Session):
        return db.query(Logs).all()