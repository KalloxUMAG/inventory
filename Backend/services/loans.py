from sqlalchemy.orm import Session
from models.models import Loan, Lot, Users, Supply, Groups
from schemas.loans_scheme import LoanCreate
from schemas.lot_schema import CreateLotSchema

from services.lots import LotService
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

lotService = LotService()

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
        lot = await lotService.get_lot_to_loan(loan.lot_id, db)
        new_lot = CreateLotSchema(number=lot.number, supply_id=lot.supplies_id, group_id=lot.group_id, supplier_id=lot.supplier_id, stock=0)
        await lotService.update_lot(user_id=user_id, lot=lot, data_update=new_lot, db=db)
        return new_loan
    
    @log_func_calls("loans", UPDATE_LOG)
    async def update_loan(self, user_id: int, loan_id: int, data_update: LoanCreate, db: Session):
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        loan.start_date = data_update.start_date
        loan.end_date = data_update.end_date
        loan.state = data_update.state
        loan.description = data_update.description
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan
    
    @log_func_calls("loans", DELETE_LOG)
    async def delete_loan(self, user_id: int, loan_id: int, db: Session):
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        db.delete(loan)
        db.commit()
        return loan