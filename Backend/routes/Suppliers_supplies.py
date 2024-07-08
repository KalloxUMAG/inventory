from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from services.suppliers_supplies import SupplierSupplyService
from services.suppliers import SupplierService
from services.supplies import SupplyService
from schemas.supplier_supply_schema import GetSupplierSupplySchema, SupplierSupplySchema

from auth.auth_bearer import JWTBearer, get_user_id_from_token

suppliers_supplies = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["suppliers"],
    prefix="/api/suppliers_supplies",
)
service = SupplierSupplyService()
supplier_service = SupplierService()
supply_service = SupplyService()


@suppliers_supplies.get("", response_model=List[SupplierSupplySchema])
async def get_suppliers_supplies(db: Session = Depends(get_db)):
    result = await service.get_suppliers_supplies(db)
    return result


@suppliers_supplies.post("", status_code=HTTP_201_CREATED)
async def add_supplier_supply(
    supplier_supply: SupplierSupplySchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_supplier = await supplier_service.get_supplier(supplier_supply.supplier_id, db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_supply = await supply_service.get_supply(supplier_supply.supply_id, db)
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier_supply = await service.add_supplier_supply(user_id=get_user_id_from_token(dependencies), supplier_supply=supplier_supply, db=db)
    return Response(status_code=HTTP_201_CREATED)


@suppliers_supplies.get("/{supply_id}", response_model=List[GetSupplierSupplySchema])
async def get_suppliers_supply(supply_id: int, db: Session = Depends(get_db)):
    suppliers = await service.get_suppliers_by_supply(supply_id, db)
    return suppliers
