from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from services.loans import LoanService
from schemas.loans_scheme import LoanCreate, LoanSchema
from schemas.equipment_schema import EquipmentAvailableSchema

from auth.auth_bearer import JWTBearer, get_user_id_from_token
## Depends(JWTBearer())
loans = APIRouter(
    dependencies=[], tags=["loans"], prefix="/api/loans"
)
service = LoanService()


@loans.get("/", response_model=List[LoanSchema])
async def get_loans(db: Session = Depends(get_db)):
    loans = await service.get_loans(db)
    return loans

@loans.post("/", tags=["loans"], response_model=LoanSchema)
async def create_loan(loan: LoanCreate, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    new_loan = await service.create_loan(user_id=get_user_id_from_token(dependencies), loan=loan, db=db)
    return new_loan