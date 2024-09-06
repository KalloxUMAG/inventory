from datetime import date
from typing import Optional

from pydantic import BaseModel

class LoanSchema(BaseModel):
    id: Optional[int] = None
    start_date: date
    end_date: date
    user_id: int
    user_fullname: Optional[str] = None
    lot_id: int
    lot_number: Optional[str] = None
    state: str
    description: str
    supply_id: int
    supply_name: str
    supply_code: str
    group_id: int
    group_name: str

    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    lot_id: int
    start_date: date
    end_date: date
    state: str
    description: str

    class Config:
        from_attributes = True