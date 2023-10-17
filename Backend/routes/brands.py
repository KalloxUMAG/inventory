from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

from config.database import get_db
from models.models import Brand
from schemas.brand_schema import BrandSchema

from auth.auth_bearer import JWTBearer

brands = APIRouter(dependencies=[Depends(JWTBearer())], prefix="/api/brands")


@brands.get("", response_model=List[BrandSchema])
def get_brands(db: Session = Depends(get_db)):
    result = db.query(Brand).all()
    return result


@brands.post("", status_code=HTTP_201_CREATED)
def add_brand(brand: BrandSchema, db: Session = Depends(get_db)):
    db_brand = (
        db.query(Brand).filter(func.lower(Brand.name) == brand.name.lower()).first()
    )
    if db_brand:
        content = str(db_brand.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_brand = Brand(name=brand.name)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    content = str(new_brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@brands.get("/{brand_id}", response_model=BrandSchema)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    return db.query(Brand).filter(Brand.id == brand_id).first()


@brands.put("/{brand_id}", response_model=BrandSchema)
def update_brand(
    data_update: BrandSchema, brand_id: int, db: Session = Depends(get_db)
):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_brand, key, value)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@brands.delete("/{brand_id}", status_code=HTTP_204_NO_CONTENT)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_brand)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
