from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Supplier
from schemas.supplier_schema import SupplierSchema, SupplierSchemaWithId, SupplierFullSchema
from services.supplier_contact import SupplierContactService

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
    async def add_supplier(self, supplier: SupplierFullSchema, db: Session):
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
            new_contact = {
                "name": contact.name,
                "position": contact.position,
                "phone": contact.phone,
                "email": contact.email,
                "supplier_id": new_supplier.id,
            }
            contact_service.add_supplier_contact(new_contact, db)
        return new_supplier
    async def update_supplier(self, supplier: SupplierSchemaWithId, data_update: SupplierSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(supplier, key, value)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier
    async def delete_supplier(self, supplier: SupplierSchemaWithId, db: Session):
        db.delete(supplier)
        db.commit()