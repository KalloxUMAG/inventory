from fastapi import UploadFile
from pathlib import Path
from config.settings import settings
from sqlalchemy.orm import Session
from models.models import Invoice
from schemas.invoce_schema import InvoiceSchema, InvoiceSchemaWithId

class InvoiceService:
    async def get_invoices(self, db: Session):
        return db.query(Invoice).all()
    async def get_invoice(self, invoice_id: int, db: Session):
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()
    async def get_invoices_by_supplier(self, supplier_id: int, db: Session):
        return db.query(Invoice).filter(Invoice.supplier_id == supplier_id).all()
    async def add_invoice(self, invoice: InvoiceSchema, db: Session):
        db_invoice = (
            db.query(Invoice)
            .filter(
                Invoice.number == invoice.number,
                Invoice.date == invoice.date,
                Invoice.supplier_id == invoice.supplier_id,
            )
            .first()
        )
        if db_invoice:
            return db_invoice
        new_invoice = Invoice(
            number=invoice.number, date=invoice.date, supplier_id=invoice.supplier_id
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        return new_invoice
    async def add_invoice_image(self, invoice_id: int, file: UploadFile):
        image_path = Path(settings.image_directory, "invoices", str(invoice_id))
        image_path.mkdir(parents=True, exist_ok=True)
        with open(image_path / file.filename, "wb") as buffer:
            buffer.write(await file.read())
    async def delete_invoice(self, invoice: InvoiceSchemaWithId, db: Session):
        db.delete(invoice)
        db.commit()
        return None