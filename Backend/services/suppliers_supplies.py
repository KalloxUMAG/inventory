from sqlalchemy.orm import Session
from models.models import SuppliersHasSupplies, Supplier
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class SupplierSupplyService:
    async def get_suppliers_supplies(self, db: Session):
        return db.query(SuppliersHasSupplies).all()
    async def get_suppliers_by_supply(self, supply_id: int, db: Session):
        result = (
            db.query(
                SuppliersHasSupplies.supplier_id,
                SuppliersHasSupplies.supply_id,
                SuppliersHasSupplies.cost,
                Supplier.name.label("name"),
                Supplier.rut.label("rut"),
                Supplier.city_address.label("city_address"),
            )
            .filter(SuppliersHasSupplies.supply_id == supply_id)
            .outerjoin(Supplier, Supplier.id == SuppliersHasSupplies.supplier_id)
            .all()
        )
        return result
    async def add_supplier_supply(self, user_id: int, supplier_supply: SuppliersHasSupplies, db: Session):
        new_supplier_supply = SuppliersHasSupplies(
            supplier_id=supplier_supply.supplier_id,
            supply_id=supplier_supply.supply_id,
            cost=supplier_supply.cost,
        )
        db.add(new_supplier_supply)
        db.commit()
        db.refresh(new_supplier_supply)
        return new_supplier_supply