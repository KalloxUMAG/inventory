from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    target_id: int
    target_table: str
    action: str
    date: datetime
    new_data: dict

    class Config:
        from_attributes = True