from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Supplies, Supplies_brand, Supplies_types, Suppliers
from schemas.supply_schema import SupplyListSchema, SupplySchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

supplies = APIRouter()


@supplies.get("/api/supplies", response_model=List[SupplyListSchema])
def get_supplies(db: Session = Depends(get_db)):
    result = (
        db.query(
            Supplies.id,
            Supplies.name,
            Supplies.code,
            Supplies.cost,
            Supplies.stock,
            Supplies.critical_stock,
            Supplies_brand.name.label("supplies_brand_name"),
            Supplies_types.name.label("supplies_type_name"),
        )
        .outerjoin(Supplies_brand, Supplies_brand.id == Supplies.supplies_brand_id)
        .outerjoin(Supplies_types, Supplies_types.id == Supplies.supplies_type_id)
        .all()
    )
    return result


@supplies.post("/api/supplies", status_code=HTTP_201_CREATED)
def add_supplies(supply: SupplySchema, db: Session = Depends(get_db)):
    new_supply = Supplies(
        name=supply.name,
        code=supply.code,
        cost=supply.cost,
        stock=supply.stock,
        samples=supply.samples,
        critical_stock=supply.critical_stock,
        supplies_brand_id=supply.supplies_brand_id,
        supplies_type_id=supply.supplies_type_id,
    )
    db.add(new_supply)
    db.commit()
    db.refresh(new_supply)
    content = str(new_supply)
    return Response(status_code=HTTP_201_CREATED, content=content)


@supplies.get("/api/supplies/{supply_id}", response_model=SupplyListSchema)
def get_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Supplies.id,
            Supplies.name,
            Supplies.code,
            Supplies.cost,
            Supplies.stock,
            Supplies.critical_stock,
            Supplies.samples,
            Supplies_brand.name.label("supplies_brand_name"),
            Supplies_types.name.label("supplies_type_name"),
        )
        .outerjoin(Supplies_brand, Supplies_brand.id == Supplies.supplies_brand_id)
        .outerjoin(Supplies_types, Supplies_types.id == Supplies.supplies_type_id)
        .filter(Supplies.id == supply_id)
        .first()
    )
    return result
