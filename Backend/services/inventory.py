from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import Session
from models.models import Equipment, Loan, Users
from schemas.loans_scheme import LoanCreate

from helpers.utils import format_equipment_data

class LoanService:
    async def get_loans(self, db: Session):
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
    async def get_equipments_with_availability(self, start_date: date, end_date: date, db: Session):
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
    
    async def get_equipment_availability(self, equipment_id: int, start_date: date, end_date: date, db: Session):
        return db.query(Loan).filter(
            Loan.equipment_id == equipment_id,
            Loan.loan_start_date <= end_date,
            Loan.loan_end_date >= start_date,
        ).first()

    async def create_loan(self, loan: LoanCreate, db: Session):
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