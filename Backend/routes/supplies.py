from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from config.database import get_db
from services.supplies import SupplyService
from schemas.supply_schema import (
    SupplyListSchema,
    SupplySchema,
    SupplySchemaFull,
    UpdateStockSchema,
    SupplyCriticalSchema
)

from auth.auth_bearer import JWTBearer, get_user_id_from_token

from dependencies.permissions import check_permissions_factory

supplies = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["supplies"], prefix="/api/supplies"
)
service = SupplyService()


@supplies.get("", response_model=List[SupplyListSchema])
async def get_supplies(db: Session = Depends(get_db)):
   supplies = await service.get_supplies(db)
   return supplies


@supplies.get("/by_group/{group_id}", response_model=List[SupplySchema])
async def get_supplies_by_group(group_id: int, db: Session = Depends(get_db)):
    supplies = await service.get_supplies_by_group(group_id, db)
    return supplies

@supplies.get("/critical", response_model=List[SupplyCriticalSchema])
async def get_supplies_critical(db: Session = Depends(get_db)):
    supplies = await service.get_supplies_critical(db)
    return supplies


@supplies.post("", status_code=HTTP_201_CREATED)
async def add_supplies(supply: SupplySchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_supply = await service.get_supply_by_code(supply.code, db)
    if db_supply:
        return Response(status_code=HTTP_409_CONFLICT)
    new_supply = await service.add_supply(user_id=get_user_id_from_token(dependencies), supply=supply, db=db)
    content = str(new_supply.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@supplies.get("/{supply_id}", response_model=SupplySchemaFull)
async def get_supply(supply_id: int, db: Session = Depends(get_db)):
    supply = await service.get_supply(supply_id, db)
    if not supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return supply


@supplies.put("/stock/{supply_id}", response_model=SupplySchema)
async def update_stock(
    data_update: UpdateStockSchema, supply_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_supply = await service.get_supply(supply_id, db)
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_supply = await service.update_stock(user_id=get_user_id_from_token(dependencies), data_update=data_update, supply=db_supply, db=db)
    return update_supply


@supplies.put("/{supply_id}", response_model=SupplySchema)
async def update_supply(
    data_update: SupplySchema, supply_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_supply = await service.get_supply_simple(supply_id, db)
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_supply = await service.update_supply(user_id=get_user_id_from_token(dependencies), data_update=data_update, supply=db_supply, db=db)
    return update_supply


@supplies.delete("/{supply_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_supply(supply_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_supply = await service.get_supply(supply_id, db)
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    delete_supply = await service.delete_supply(user_id=get_user_id_from_token(dependencies), supply=db_supply, db=db)
    return delete_supply
