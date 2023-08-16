from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from models.models import SupplyBrand
from schemas.supplies_brand_schema import SuppliesBrandsSchema

supplies_brands = APIRouter()


@supplies_brands.get(
    "/api/supplies_brands", response_model=List[SuppliesBrandsSchema], tags=["supplies"]
)
def get_supplies_brands(db: Session = Depends(get_db)):
    result = db.query(SupplyBrand.id, SupplyBrand.name).all()
    return result


@supplies_brands.post("/api/supplies_brands", status_code=HTTP_201_CREATED, tags=["supplies"])
def add_supplies_brand(brand: SuppliesBrandsSchema, db: Session = Depends(get_db)):
    new_supplies_brand = SupplyBrand(name=brand.name)
    db.add(new_supplies_brand)
    db.commit()
    db.refresh(new_supplies_brand)
    content = str(new_supplies_brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
