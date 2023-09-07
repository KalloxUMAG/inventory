from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import SupplierContact
from routes.suppliers import get_supplier
from schemas.supplier_contact_schema import SupplierContactSchema

from auth.auth_bearer import JWTBearer

suppliers_contacts = APIRouter(dependencies=[Depends(JWTBearer())], tags=["suppliers"])


@suppliers_contacts.get(
    "/api/suppliers_contacts", response_model=List[SupplierContactSchema]
)
def get_suppliers_contacts(db: Session = Depends(get_db)):
    result = db.query(SupplierContact).all()
    return result


@suppliers_contacts.post("/api/suppliers_contacts", status_code=HTTP_201_CREATED)
def add_supplier_contact(
    supplier_contact: SupplierContactSchema, db: Session = Depends(get_db)
):
    db_supplier = get_supplier(supplier_contact.supplier_id, db=db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
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
    return Response(status_code=HTTP_201_CREATED)


@suppliers_contacts.get(
    "/api/suppliers_contacts/{supplier_contact_id}",
    response_model=SupplierContactSchema,
)
def get_supplier_contact(supplier_contact_id: int, db: Session = Depends(get_db)):
    return (
        db.query(SupplierContact)
        .filter(SupplierContact.id == supplier_contact_id)
        .first()
    )


@suppliers_contacts.get(
    "/api/supplier_contacts/{supplier_id}", response_model=List[SupplierContactSchema]
)
def get_supplier_contacts(supplier_id: int, db: Session = Depends(get_db)):
    return (
        db.query(SupplierContact)
        .filter(SupplierContact.supplier_id == supplier_id)
        .all()
    )


@suppliers_contacts.put(
    "/api/suppliers_contacts/{supplier_contact_id}",
    response_model=SupplierContactSchema,
)
def update_supplier_contact(
    data_update: SupplierContactSchema,
    supplier_contact_id: int,
    db: Session = Depends(get_db),
):
    db_supplier_contact = get_supplier_contact(supplier_contact_id, db=db)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_supplier_contact, key, value)
    db.add(db_supplier_contact)
    db.commit()
    db.refresh(db_supplier_contact)
    return db_supplier_contact


@suppliers_contacts.delete(
    "/api/suppliers_contacts/{supplier_contact_id}", status_code=HTTP_204_NO_CONTENT
)
def delete_supplier_contact(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier_contact = get_supplier_contact(supplier_id, db=db)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_supplier_contact)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
