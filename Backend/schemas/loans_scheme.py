from datetime import date
from typing import Optional

from pydantic import BaseModel

class LoanSchema(BaseModel):
    loan_id: Optional[int] = None
    loan_start_date: date
    loan_end_date: date
    user_fullname: str
    user_email: str
    equipment_id: int
    equipment_name: str
    user_id: int

    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    user_id: int
    equipment_id: int
    loan_start_date: date
    loan_end_date: date