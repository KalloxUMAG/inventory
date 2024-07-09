from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from config.database import get_db
from services.supplies_types import SupplyTypeService
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

supplies_types = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["supplies"], prefix="/api/supplies_types"
)
service = SupplyTypeService()


@supplies_types.get("", response_model=List[BasicOptionSchemaWithId])
async def get_supplies_types(db: Session = Depends(get_db)):
    supply_types = await service.get_supply_types(db)
    return supply_types


@supplies_types.post("", status_code=HTTP_201_CREATED)
async def add_supplies_type(type: BasicOptionSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    supply_type = await service.add_supply_type(user_id=get_user_id_from_token(dependencies), db=db, supply_type_name=type.name)
    content = str(supply_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
