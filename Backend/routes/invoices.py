from typing import List

from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.invoices import InvoiceService
from schemas.invoce_schema import InvoiceSchema, InvoiceSchemaWithId

from auth.auth_bearer import JWTBearer

invoices = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["invoices"], prefix="/api/invoices"
)
service = InvoiceService()


@invoices.get("", response_model=List[InvoiceSchemaWithId])
async def get_inovices(db: Session = Depends(get_db)):
    invoices = await service.get_invoices(db)
    return invoices


@invoices.post("", status_code=HTTP_201_CREATED)
async def add_invoice(invoice: InvoiceSchema, db: Session = Depends(get_db)):
    new_invoice = await service.add_invoice(invoice, db)
    content = str(new_invoice.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


# Upload image to invoice folder using invoice id
@invoices.post("/{invoice_id}", status_code=HTTP_201_CREATED)
async def add_image(invoice_id: int, file: UploadFile):
    await service.add_invoice_image(invoice_id, file)
    return Response(status_code=HTTP_201_CREATED)


@invoices.get("/{invoice_id}", response_model=InvoiceSchemaWithId)
async def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = await service.get_invoice(invoice_id, db)
    if not invoice:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return invoice


# Get invoice by supplier_id
@invoices.get("/supplier/{supplier_id}", response_model=List[InvoiceSchemaWithId])
async def get_invoice_supplier(supplier_id: int, db: Session = Depends(get_db)):
    invoices = await service.get_invoices_by_supplier(supplier_id, db)
    return invoices


@invoices.delete("/{invoice_id}", status_code=HTTP_200_OK)
async def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = await service.get_invoice(invoice_id, db=db)
    if not db_invoice:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_invoice(db_invoice, db)
    return Response(status_code=HTTP_200_OK)
