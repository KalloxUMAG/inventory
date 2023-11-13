from datetime import date
from typing import Optional

from pydantic import BaseModel


class LoanSchema(BaseModel):
    loan_id: Optional[int] = None
    user_id: int
    equipment_id: int
    loan_start_date: date
    loan_end_date: date

    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    user_id: int
    equipment_id: int
    loan_start_date: date
    loan_end_date: date