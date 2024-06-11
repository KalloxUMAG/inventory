from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import Supplier, SupplierContact
from schemas.supplier_schema import SupplierSchema, SupplierFullSchema
from routes.supplier_contact import get_supplier_contacts

from auth.auth_bearer import JWTBearer

suppliers = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["suppliers"], prefix="/api/suppliers"
)


@suppliers.get("", response_model=List[SupplierSchema])
def get_suppliers(db: Session = Depends(get_db)):
    result = db.query(Supplier).all()
    return result

@suppliers.get("/full", response_model=List[SupplierFullSchema])
def get_suppliers_full(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    new_suppliers = [{
        "id": supplier.id,
        "name": supplier.name,
        "rut": supplier.rut,
        "city_address": supplier.city_address,
        "contacts": get_supplier_contacts(supplier.id, db)
    } for supplier in suppliers]
    return new_suppliers

@suppliers.post("", status_code=HTTP_201_CREATED)
def add_supplier(supplier: SupplierFullSchema, db: Session = Depends(get_db)):
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
        content = str(db_supplier.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_supplier = Supplier(
        name=supplier.name, rut=supplier.rut, city_address=supplier.city_address
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    for contact in supplier.contacts:
        new_contact = SupplierContact(
            name=contact.name,
            position=contact.position,
            phone=contact.phone,
            email=contact.email,
            supplier_id=new_supplier.id,
        )
        db.add(new_contact)
    db.commit()
    content = str(new_supplier.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@suppliers.get("/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


@suppliers.put("/{supplier_id}", response_model=SupplierSchema)
def update_supplier(
    data_update: SupplierSchema, supplier_id: int, db: Session = Depends(get_db)
):
    db_supplier = get_supplier(supplier_id, db=db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@suppliers.delete("/{supplier_id}", status_code=HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = get_supplier(supplier_id, db=db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_supplier)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
