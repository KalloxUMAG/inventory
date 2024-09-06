from sqlalchemy.orm import Session
from models.models import Loan, Lot, Users, Supply, Groups
from schemas.loans_scheme import LoanCreate

from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class LoanService:
    async def get_loans(self, db: Session):
        result = (
            db.query(
                Loan.id,
                Loan.start_date,
                Loan.end_date,
                Loan.state,
                Loan.description,
                Users.fullname.label("user_fullname"),
                Users.id.label("user_id"),
                Lot.id.label("lot_id"),
                Lot.number.label("lot_number"),
                Supply.id.label("supply_id"),
                Supply.name.label("supply_name"),
                Supply.code.label("supply_code"),
                Groups.id.label("group_id"),
                Groups.name.label("group_name"),
            )
            .join(Users, Users.id == Loan.user_id)
            .join(Lot, Lot.id == Loan.lot_id)
            .join(Supply, Supply.id == Lot.supplies_id)
            .join(Groups, Groups.id == Lot.group_id)
            .all()
        )
        return result

    @log_func_calls("loans", CREATE_LOG)
    async def create_loan(self, user_id: int, loan: LoanCreate, db: Session):
        new_loan = Loan(
            user_id=user_id,
            lot_id=loan.lot_id,
            start_date=loan.start_date,
            end_date=loan.end_date,
            state=loan.state,
            description=loan.description,
        )
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan