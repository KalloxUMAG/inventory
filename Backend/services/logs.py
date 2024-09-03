from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Logs
from schemas.log_schema import LogSchema

from datetime import datetime
from typing import Callable
from functools import wraps

CREATE_LOG = "create"
UPDATE_LOG = "update"
DELETE_LOG = "delete"

class LogService:
    async def get_logs(self, db: Session):
        return db.query(Logs).all()
    async def add_log(self, log: LogSchema, db: Session):
        new_log = Logs(
            user_id=log.user_id,
            target_id=log.target_id,
            target_table=log.target_table,
            action=log.action,
            date=log.date,
            new_data=log.new_data
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

def log_func_calls(table_name: str, log_method: str):
    def wrapper(func: Callable):
        @wraps(func)
        async def wrapper_func(*args, **kwargs):            
            try:
                response = await func(*args, **kwargs)
            except Exception as e:
                print(e)
                raise e
            else:
                user_id = kwargs["user_id"]
                current_date = datetime.now()
                target_id = response.id
                new_data = {}
                if log_method == CREATE_LOG:
                    new_data = row2dict(response)
                if log_method == UPDATE_LOG:
                    data = kwargs["data_update"].dict()
                    new_data = del_dict_nulls(data)
                log = LogSchema(
                    user_id=user_id,
                    target_id=target_id,
                    target_table=table_name,
                    action=log_method,
                    date=current_date,
                    new_data=new_data
                )
                await LogService().add_log(log, kwargs["db"])
                return response
        return wrapper_func
    return wrapper

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        if len(str(getattr(row, column.name))) != 0:
            d[column.name] = str(getattr(row, column.name))

    return d

def del_dict_nulls(d: dict):
    new_dict = {}
    for key, value in d.items():
        if value != None:
            new_dict[key] = str(d[key])
    return new_dict