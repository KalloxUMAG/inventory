from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import SupplierContact
from schemas.supplier_contact_schema import SupplierContactSchema, SupplierContactSchemaWithId

class SupplierContactService:
    async def get_supplier_contacts(self, db: Session):
        return db.query(SupplierContact).all()
    async def get_supplier_contact(self, supplier_contact_id: int, db: Session):
        return db.query(SupplierContact).filter(SupplierContact.id == supplier_contact_id).first()
    async def get_supplier_contact_by_supplier(self, supplier_id: int, db: Session):
        return db.query(SupplierContact).filter(SupplierContact.supplier_id == supplier_id).all()
    async def add_supplier_contact(self, supplier_contact: SupplierContactSchema, db: Session):
        db_supplier_contact = (
            db.query(SupplierContact)
            .filter(
                func.lower(SupplierContact.name) == supplier_contact.name.lower(),
                func.lower(SupplierContact.position) == supplier_contact.position.lower(),
                func.lower(SupplierContact.email) == supplier_contact.email.lower(),
                SupplierContact.supplier_id == supplier_contact.supplier_id,
            )
            .first()
        )
        if db_supplier_contact:
            return db_supplier_contact
        new_supplier_contact = SupplierContact(
            name=supplier_contact.name,
            position=supplier_contact.position,
            phone=supplier_contact.phone,
            email=supplier_contact.email,
            supplier_id=supplier_contact.supplier_id,
        )
        db.add(new_supplier_contact)
        db.commit()
        db.refresh(new_supplier_contact)
        return new_supplier_contact
    async def update_supplier_contact(self, supplier_contact: SupplierContactSchemaWithId, data_update: SupplierContactSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(supplier_contact, key, value)
        db.add(supplier_contact)
        db.commit()
        db.refresh(supplier_contact)
        return supplier_contact
    async def delete_supplier_contact(self, supplier_contact: SupplierContactSchemaWithId, db: Session):
        db.delete(supplier_contact)
        db.commit()