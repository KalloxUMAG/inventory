from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from services.supplies_brands import SupplyBrandService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer

supplies_brands = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["supplies"],
    prefix="/api/supplies_brands",
)
service = SupplyBrandService()

@supplies_brands.get("", response_model=List[BasicOptionSchemaWithId])
async def get_supplies_brands(db: Session = Depends(get_db)):
    supplies_brands = await service.get_supply_brands(db)
    return supplies_brands


@supplies_brands.post("", status_code=HTTP_201_CREATED)
async def add_supplies_brand(brand: BasicOptionSchema, db: Session = Depends(get_db)):
    supply_brand = await service.add_supply_brand(supply_brand_name=brand.name, db=db)
    content = str(supply_brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
