from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Supplier, SuppliersHasSupplies, Supply
from schemas.supplier_supply_schema import GetSupplierSupplySchema, SupplierSupplySchema

from auth.auth_bearer import JWTBearer

suppliers_supplies = APIRouter(dependencies=[Depends(JWTBearer())], tags=["suppliers"])


@suppliers_supplies.get(
    "/api/suppliers_supplies", response_model=List[SupplierSupplySchema]
)
def get_suppliers_supplies(db: Session = Depends(get_db)):
    result = db.query(SuppliersHasSupplies).all()
    return result


@suppliers_supplies.post("/api/suppliers_supplies", status_code=HTTP_201_CREATED)
def add_supplier_supply(
    supplier_supply: SupplierSupplySchema, db: Session = Depends(get_db)
):
    db_supplier = (
        db.query(Supplier).filter(Supplier.id == supplier_supply.supplier_id).first()
    )
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_supply = db.query(Supply).filter(Supply.id == supplier_supply.supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier_supply = SuppliersHasSupplies(
        supplier_id=supplier_supply.supplier_id,
        supply_id=supplier_supply.supply_id,
        cost=supplier_supply.cost,
    )
    db.add(new_supplier_supply)
    db.commit()
    db.refresh(new_supplier_supply)
    return Response(status_code=HTTP_201_CREATED)


@suppliers_supplies.get(
    "/api/suppliers_supplies/{supply_id}", response_model=List[GetSupplierSupplySchema]
)
def get_suppliers_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            SuppliersHasSupplies.supplier_id,
            SuppliersHasSupplies.supply_id,
            SuppliersHasSupplies.cost,
            Supplier.name.label("name"),
            Supplier.rut.label("rut"),
            Supplier.city_address.label("city_address"),
        )
        .filter(SuppliersHasSupplies.supply_id == supply_id)
        .outerjoin(Supplier, Supplier.id == SuppliersHasSupplies.supplier_id)
        .all()
    )
    return result
