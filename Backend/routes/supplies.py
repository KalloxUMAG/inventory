from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Supply, SupplyBrand, SupplyFormat, SupplyType
from schemas.supply_schema import (
    SupplyListSchema,
    SupplySchema,
    SupplySchemaFull,
    UpdateStockSchema,
)

supplies = APIRouter()


@supplies.get("/api/supplies", response_model=List[SupplyListSchema], tags=["supplies"])
def get_supplies(db: Session = Depends(get_db)):
    result = (
        db.query(
            Supply.id,
            Supply.name,
            Supply.code,
            Supply.state,
            Supply.stock,
            Supply.lot_stock,
            Supply.samples,
            Supply.critical_stock,
            Supply.observation,
            SupplyBrand.name.label("supplies_brand_name"),
            SupplyType.name.label("supplies_type_name"),
            SupplyFormat.name.label("supplies_format_name"),
        )
        .outerjoin(SupplyBrand, SupplyBrand.id == Supply.supplies_brand_id)
        .outerjoin(SupplyType, SupplyType.id == Supply.supplies_type_id)
        .outerjoin(SupplyFormat, SupplyFormat.id == Supply.supplies_format_id)
        .filter(Supply.state is True)
        .all()
    )
    return result


@supplies.get("/api/supplies/critical", response_model=List[SupplyListSchema], tags=["supplies"])
def get_supplies_critical(db: Session = Depends(get_db)):
    result = (
        db.query(
            Supply.id,
            Supply.name,
            Supply.code,
            Supply.stock,
            Supply.lot_stock,
            Supply.samples,
            Supply.critical_stock,
            Supply.observation,
            SupplyBrand.name.label("supplies_brand_name"),
            SupplyType.name.label("supplies_type_name"),
            SupplyFormat.name.label("supplies_format_name"),
        )
        .outerjoin(SupplyBrand, SupplyBrand.id == Supply.supplies_brand_id)
        .outerjoin(SupplyType, SupplyType.id == Supply.supplies_type_id)
        .outerjoin(SupplyFormat, SupplyFormat.id == Supply.supplies_format_id)
        .filter(and_(Supply.stock <= Supply.critical_stock, Supply.state is True))
        .all()
    )
    return result


@supplies.post("/api/supplies", status_code=HTTP_201_CREATED, tags=["supplies"])
def add_supplies(supply: SupplySchema, db: Session = Depends(get_db)):
    new_supply = Supply(
        name=supply.name,
        code=supply.code,
        state=True,
        stock=supply.stock,
        samples=supply.samples,
        observation=supply.observation,
        critical_stock=supply.critical_stock,
        lot_stock=supply.lot_stock,
        supplies_brand_id=supply.supplies_brand_id,
        supplies_format_id=supply.supplies_format_id,
        supplies_type_id=supply.supplies_type_id,
    )
    db.add(new_supply)
    db.commit()
    db.refresh(new_supply)
    content = str(new_supply.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@supplies.get("/api/supplies/{supply_id}", response_model=SupplySchemaFull, tags=["supplies"])
def get_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Supply.id,
            Supply.name,
            Supply.code,
            Supply.state,
            Supply.stock,
            Supply.critical_stock,
            Supply.lot_stock,
            Supply.samples,
            Supply.observation,
            Supply.supplies_brand_id,
            Supply.supplies_format_id,
            Supply.supplies_type_id,
            SupplyBrand.name.label("supplies_brand_name"),
            SupplyType.name.label("supplies_type_name"),
            SupplyFormat.name.label("supplies_format_name"),
        )
        .filter(and_(Supply.id == supply_id, Supply.state is True))
        .outerjoin(SupplyBrand, SupplyBrand.id == Supply.supplies_brand_id)
        .outerjoin(SupplyType, SupplyType.id == Supply.supplies_type_id)
        .outerjoin(SupplyFormat, SupplyFormat.id == Supply.supplies_format_id)
        .first()
    )
    if result is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return result


@supplies.put("/api/supplies/stock/{supply_id}", response_model=SupplySchema, tags=["supplies"])
def update_stock(data_update: UpdateStockSchema, supply_id: int, db: Session = Depends(get_db)):
    db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_supply, "stock", db_supply.stock + data_update.stock)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply


@supplies.put("/api/supplies/{supply_id}", response_model=SupplySchema, tags=["supplies"])
def update_supply(data_update: SupplySchema, supply_id: int, db: Session = Depends(get_db)):
    db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_supply, key, value)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply


@supplies.delete("/api/supplies/{supply_id}", status_code=HTTP_204_NO_CONTENT, tags=["supplies"])
def delete_supply(supply_id: int, db: Session = Depends(get_db)):
    db_supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_supply, "state", False)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply
