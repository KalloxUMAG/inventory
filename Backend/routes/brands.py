from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

from config.database import get_db
from services.brands import BrandService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer

brands = APIRouter(dependencies=[Depends(JWTBearer())], prefix="/api/brands")
service = BrandService()

@brands.get("", response_model=List[BasicOptionSchemaWithId])
async def get_brands(db: Session = Depends(get_db)):
    brands = await service.get_brands(db=db)
    return brands


@brands.post("", status_code=HTTP_201_CREATED)
async def add_brand(brand: BasicOptionSchema, db: Session = Depends(get_db)):
    brand = await service.add_brand(brand_name=brand.name, db=db)
    content = str(brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@brands.get("/{brand_id}", response_model=BasicOptionSchemaWithId)
async def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = await service.get_brand(brand_id=brand_id, db=db)
    if not brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return brand


@brands.put("/{brand_id}", response_model=BasicOptionSchemaWithId)
async def update_brand(
    data_update: BasicOptionSchema, brand_id: int, db: Session = Depends(get_db)
):
    db_brand = await service.get_brand(brand_id=brand_id, db=db)
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    brand = await service.update_brand(brand=db_brand, data_update=data_update, db=db)
    return brand


@brands.delete("/{brand_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = await service.get_brand(brand_id=brand_id, db=db)
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_brand(brand=db_brand, db=db)
    return Response(status_code=HTTP_200_OK)
