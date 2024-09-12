from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Supplier
from schemas.supplier_schema import SupplierSchema, SupplierSchemaWithId, SupplierFullSchema
from schemas.supplier_contact_schema import SupplierContactSchema
from services.supplier_contact import SupplierContactService
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

contact_service = SupplierContactService()

class SupplierService:
    async def get_suppliers(self, db: Session):
        return db.query(Supplier).all()
    async def get_supplier(self, supplier_id: int, db: Session):
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()
    async def get_suppliers_full(self, db: Session):
        suppliers = await self.get_suppliers(db)
        return [{
            "id": supplier.id,
            "name": supplier.name,
            "rut": supplier.rut,
            "city_address": supplier.city_address,
            "contacts": await contact_service.get_supplier_contact_by_supplier(supplier.id, db)
        } for supplier in suppliers]
    @log_func_calls("suppliers", CREATE_LOG)
    async def add_supplier(self, user_id: int, supplier: SupplierFullSchema, db: Session):
        db_supplier = (
            db.query(Supplier)
            .filter(
                func.lower(Supplier.name) == supplier.name.lower(),
                func.lower(Supplier.rut) == supplier.rut.lower(),
                func.lower(Supplier.city_address) == supplier.city_address.lower(),
            )
            .first()
        )
        if db_supplier:
            return db_supplier
        new_supplier = Supplier(
            name=supplier.name, rut=supplier.rut, city_address=supplier.city_address
        )
        db.add(new_supplier)
        db.commit()
        db.refresh(new_supplier)
        for contact in supplier.contacts:
            new_contact = SupplierContactSchema(name=contact.name, position=contact.position, phone=contact.phone, email=contact.email, supplier_id=new_supplier.id)
            await contact_service.add_supplier_contact(user_id=user_id, supplier_contact=new_contact, db=db)
        return new_supplier
    @log_func_calls("suppliers", UPDATE_LOG)
    async def update_supplier(self, user_id: int, supplier: SupplierSchemaWithId, data_update: SupplierSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(supplier, key, value)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier
    @log_func_calls("suppliers", DELETE_LOG)
    async def delete_supplier(self, user_id: int, supplier: SupplierSchemaWithId, db: Session):
        db.delete(supplier)
        db.commit()
        return supplier