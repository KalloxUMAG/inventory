from typing import List
from datetime import date

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.loans import LoanService
from schemas.loans_scheme import LoanCreate, LoanSchema, LoanUpdateSchema

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

@loans.post("/", status_code=HTTP_201_CREATED)
async def create_loan(loan: LoanCreate, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    await service.create_loan(user_id=get_user_id_from_token(dependencies), loan=loan, db=db)
    return Response(status_code=HTTP_201_CREATED)

@loans.put("/{loan_id}", status_code=HTTP_200_OK)
async def update_loan(
    data_update: LoanUpdateSchema, loan_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    await service.update_loan(user_id=get_user_id_from_token(dependencies), loan_id=loan_id, data_update=data_update, db=db)
    return Response(status_code=HTTP_200_OK)

@loans.delete("/{loan_id}", status_code=HTTP_200_OK)
async def delete_loan(loan_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    await service.delete_loan(user_id=get_user_id_from_token(dependencies), loan_id=loan_id, db=db)
    return Response(status_code=HTTP_200_OK)