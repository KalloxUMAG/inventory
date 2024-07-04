from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from services.inventory import LoanService
from schemas.loans_scheme import LoanCreate, LoanSchema
from schemas.equipment_schema import EquipmentAvailableSchema

from auth.auth_bearer import JWTBearer
## Depends(JWTBearer())
inventory = APIRouter(
    dependencies=[], tags=["inventory"], prefix="/api/inventory"
)
service = LoanService()


@inventory.get("/loans", response_model=List[LoanSchema])
async def get_loans(db: Session = Depends(get_db)):
    loans = await service.get_loans(db)
    return loans


@inventory.get("/get_equipments_with_availability", response_model=List[EquipmentAvailableSchema])
async def get_equipments_with_availability(start_date: date, end_date: date, db: Session = Depends(get_db)):
    # Obtén todos los equipos y sus préstamos entre las fechas dadas
    equipments = await service.get_equipments_with_availability(start_date, end_date, db)
    return equipments


@inventory.post("/loans", tags=["loans"], response_model=LoanSchema)
async def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Comprueba si el equipo ya está prestado durante las fechas especificadas
    existing_loan = await service.get_equipment_availability(loan.equipment_id, loan.loan_start_date, loan.loan_end_date, db)
    if existing_loan is not None:
        raise HTTPException(status_code=400, detail="Equipment is already loaned during the specified dates")
    new_loan = await service.create_loan(loan, db)
    return new_loan