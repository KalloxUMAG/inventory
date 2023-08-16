import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import Invoice
from schemas.invoce_schema import InvoiceSchema

invoices = APIRouter()


@invoices.get("/api/invoices", response_model=List[InvoiceSchema])
def get_inovices(db: Session = Depends(get_db)):
    result = db.query(Invoice).all()
    return result


@invoices.post("/api/invoices", status_code=HTTP_201_CREATED)
async def add_invoice(invoice: InvoiceSchema, db: Session = Depends(get_db)):
    new_invoice = Invoice(number=invoice.number, date=invoice.date, supplier_id=invoice.supplier_id)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    content = str(new_invoice.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


# Upload image to invoice folder using invoice id
@invoices.post("/api/invoices/{invoice_id}", status_code=HTTP_201_CREATED)
async def add_image(invoice_id: int, file: UploadFile):
    if not os.path.exists(f"./images/invoices/{invoice_id}"):
        os.makedirs(f"./images/invoices/{invoice_id}")
    with open(f"./images/invoices/{invoice_id}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return Response(status_code=HTTP_201_CREATED)


@invoices.get("/api/invoices/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


# Get invoice by supplier_id
@invoices.get("/api/invoices/supplier/{supplier_id}", response_model=List[InvoiceSchema])
def get_invoice_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return db.query(Invoice).filter(Invoice.supplier_id == supplier_id).all()


@invoices.delete("/api/invoices/{invoice_id}", status_code=HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = get_invoice(invoice_id, db=db)
    if not db_invoice:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_invoice)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
