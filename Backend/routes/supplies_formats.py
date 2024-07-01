from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from services.supplies_formats import SupplyFormatService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer

supplies_formats = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["supplies"],
    prefix="/api/supplies_formats",
)
service = SupplyFormatService()


@supplies_formats.get("", response_model=List[BasicOptionSchemaWithId])
async def get_supplies_formats(db: Session = Depends(get_db)):
    supply_formats = await service.get_supply_formats(db)
    return supply_formats


@supplies_formats.post("", status_code=HTTP_201_CREATED)
async def add_supplies_format(supply_format: BasicOptionSchema, db: Session = Depends(get_db)):
    supply_format = await service.add_supply_format(db=db, supply_format_name=supply_format.name)
    content = str(supply_format.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
