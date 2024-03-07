from typing import List
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from helpers.utils import format_equipment_data
from models.models import Equipment, Loan, Maintenance, Users
from routes.equipments import get_equipment_exist
from schemas.loans_scheme import LoanCreate, LoanSchema
from schemas.equipment_schema import EquipmentAvailableSchema, EquipmentSchema
from schemas.maintenance_schema import (
    EditMaintenanceSchema,
    MaintenanceFromEquipment,
    MaintenanceSchema,
)


from auth.auth_bearer import JWTBearer
## Depends(JWTBearer())
inventory = APIRouter(
    dependencies=[], tags=["inventory"], prefix="/api/inventory"
)


@inventory.get("/loans", response_model=List[LoanSchema])
def get_loans(db: Session = Depends(get_db)):
    result = (
        db.query(
            Loan.loan_id,
            Loan.loan_start_date,
            Loan.loan_end_date,
            Users.fullname.label("user_fullname"),
            Users.email.label("user_email"),
            Users.id.label("user_id"),
            Equipment.id.label("equipment_id"),
            Equipment.name.label("equipment_name"),
        )
        .join(Users, Users.id == Loan.user_id)
        .join(Equipment, Equipment.id == Loan.equipment_id)
        .all()
    )
    return result


@inventory.get("/get_equipments_with_availability", response_model=List[EquipmentAvailableSchema])
def get_equipments_with_availability(start_date: date, end_date: date, db: Session = Depends(get_db)):
    # Obtén todos los equipos y sus préstamos entre las fechas dadas
    equipments_and_loans = (
        db.query(Equipment, Loan)
        .outerjoin(Loan, and_(
            Equipment.id == Loan.equipment_id,
            Loan.loan_start_date <= end_date,
            Loan.loan_end_date >= start_date
        ))
        .all()
    )

    equipments = format_equipment_data(equipments_and_loans)

    return equipments


@inventory.post("/loans", tags=["loans"], response_model=LoanSchema)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Comprueba si el equipo ya está prestado durante las fechas especificadas
    existing_loan = db.query(Loan).filter(
        Loan.equipment_id == loan.equipment_id,
        Loan.loan_start_date <= loan.loan_end_date,
        Loan.loan_end_date >= loan.loan_start_date,
    ).first()

    if existing_loan is not None:
        raise HTTPException(status_code=400, detail="Equipment is already loaned during the specified dates")

    new_loan = Loan(
        user_id=loan.user_id,
        equipment_id=loan.equipment_id,
        loan_start_date=loan.loan_start_date,
        loan_end_date=loan.loan_end_date,
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan