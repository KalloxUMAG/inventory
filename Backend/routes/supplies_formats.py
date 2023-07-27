from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Supplies_formats
from schemas.supplies_format_schema import SuppliesFormatsSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

supplies_formats = APIRouter()


@supplies_formats.get("/api/supplies_formats", response_model=List[SuppliesFormatsSchema], tags=["supplies"])
def get_supplies_formats(db: Session = Depends(get_db)):
    result = db.query(Supplies_formats.id, Supplies_formats.name).all()
    return result


@supplies_formats.post("/api/supplies_formats", status_code=HTTP_201_CREATED, tags=["supplies"])
def add_supplies_format(sformat: SuppliesFormatsSchema, db: Session = Depends(get_db)):
    new_supplies_format = Supplies_formats(name=sformat.name)
    db.add(new_supplies_format)
    db.commit()
    db.refresh(new_supplies_format)
    content = str(new_supplies_format.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
