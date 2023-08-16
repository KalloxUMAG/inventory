from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from models.models import SupplyType
from schemas.supplies_type_schema import SuppliesTypesSchema

supplies_types = APIRouter()


@supplies_types.get(
    "/api/supplies_types", response_model=List[SuppliesTypesSchema], tags=["supplies"]
)
def get_supplies_types(db: Session = Depends(get_db)):
    result = db.query(SupplyType.id, SupplyType.name).all()
    return result


@supplies_types.post("/api/supplies_types", status_code=HTTP_201_CREATED, tags=["supplies"])
def add_supplies_type(type: SuppliesTypesSchema, db: Session = Depends(get_db)):
    new_supplies_type = SupplyType(name=type.name)
    db.add(new_supplies_type)
    db.commit()
    db.refresh(new_supplies_type)
    content = str(new_supplies_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
