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
from services.supplier_contact import SupplierContactService
from models.models import SupplierContact
from schemas.supplier_contact_schema import SupplierContactSchema, SupplierContactSchemaWithId

from auth.auth_bearer import JWTBearer

suppliers_contacts = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["suppliers"],
    prefix="/api/suppliers_contacts",
)
service = SupplierContactService()


@suppliers_contacts.get("", response_model=List[SupplierContactSchemaWithId])
async def get_suppliers_contacts(db: Session = Depends(get_db)):
    contacts = await service.get_supplier_contacts(db)
    return contacts


@suppliers_contacts.post("", status_code=HTTP_201_CREATED)
async def add_supplier_contact(
    supplier_contact: SupplierContactSchema, db: Session = Depends(get_db)
):
    new_supplier_contact = await service.add_supplier_contact(supplier_contact, db)
    content = str(new_supplier_contact.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@suppliers_contacts.get(
    "/{supplier_contact_id}",
    response_model=SupplierContactSchemaWithId,
)
async def get_supplier_contact(supplier_contact_id: int, db: Session = Depends(get_db)):
    contact = await service.get_supplier_contact(supplier_contact_id, db)
    if not contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return contact


@suppliers_contacts.get(
    "/contacts/{supplier_id}", response_model=List[SupplierContactSchemaWithId]
)
async def get_supplier_contacts(supplier_id: int, db: Session = Depends(get_db)):
    contacts = await service.get_supplier_contact_by_supplier(supplier_id, db)
    return contacts


@suppliers_contacts.put(
    "/{supplier_contact_id}",
    response_model=SupplierContactSchemaWithId,
)
async def update_supplier_contact(
    data_update: SupplierContactSchema,
    supplier_contact_id: int,
    db: Session = Depends(get_db),
):
    db_supplier_contact = await service.get_supplier_contact(supplier_contact_id, db)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier_contact = await service.update_supplier_contact(db_supplier_contact, data_update, db)
    return new_supplier_contact


@suppliers_contacts.delete("/{contact_id}", status_code=HTTP_200_OK)
async def delete_supplier_contact(contact_id: int, db: Session = Depends(get_db)):
    db_supplier_contact = await service.get_supplier_contact(contact_id, db)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_supplier_contact(db_supplier_contact, db)
    return Response(status_code=HTTP_200_OK)
