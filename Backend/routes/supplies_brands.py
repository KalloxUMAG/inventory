from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from config.database import get_db
from models.models import SupplyBrand
from schemas.supplies_brand_schema import SuppliesBrandsSchema

from auth.auth_bearer import JWTBearer

supplies_brands = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["supplies"],
    prefix="/api/supplies_brands",
)


@supplies_brands.get("", response_model=List[SuppliesBrandsSchema])
def get_supplies_brands(db: Session = Depends(get_db)):
    result = db.query(SupplyBrand.id, SupplyBrand.name).all()
    return result


@supplies_brands.post("", status_code=HTTP_201_CREATED)
def add_supplies_brand(brand: SuppliesBrandsSchema, db: Session = Depends(get_db)):
    db_supplies_brand = (
        db.query(SupplyBrand)
        .filter(func.lower(SupplyBrand.name) == brand.name.lower())
        .first()
    )
    if db_supplies_brand:
        content = str(db_supplies_brand.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_supplies_brand = SupplyBrand(name=brand.name)
    db.add(new_supplies_brand)
    db.commit()
    db.refresh(new_supplies_brand)
    content = str(new_supplies_brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
