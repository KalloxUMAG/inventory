from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from services.groups_supplies import GroupSupplyService
from services.groups import GroupService
from services.supplies import SupplyService
from schemas.groups_supplies_schema import GroupSupplySchema

from auth.auth_bearer import JWTBearer, get_user_id_from_token

groups_supplies = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["groups"],
    prefix="/api/groups_supplies",
)
service = GroupSupplyService()
group_service = GroupService()
supply_service = SupplyService()


@groups_supplies.get("", response_model=List[GroupSupplySchema])
async def get_groups_supplies(db: Session = Depends(get_db)):
    result = await service.get_groups_supplies(db)
    return result


@groups_supplies.post("", status_code=HTTP_201_CREATED)
async def add_group_supply(group_supply: GroupSupplySchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_group = await group_service.get_group_simple(group_supply.group_id, db)
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_supply = await supply_service.get_supply(group_supply.supply_id, db)
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_group_supply = await service.add_group_supply(user_id=get_user_id_from_token(dependencies), group_supply=group_supply, db=db)
    return Response(status_code=HTTP_201_CREATED)


@groups_supplies.put("", response_model=GroupSupplySchema)
async def update_quantity(data_update: GroupSupplySchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_relation = await service.get_group_supply(data_update.group_id, data_update.supply_id, db)
    if not db_relation:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_quantity = await service.update_quantity(user_id=get_user_id_from_token(dependencies), relation=db_relation, data_update=data_update, db=db)
    return update_quantity
