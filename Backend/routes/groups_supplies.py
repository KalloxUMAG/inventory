from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import GroupsHasSupplies, Groups, Supply
from schemas.groups_supplies_schema import GroupSupplySchema

from auth.auth_bearer import JWTBearer

groups_supplies = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["groups"],
    prefix="/api/groups_supplies",
)


@groups_supplies.get("", response_model=List[GroupSupplySchema])
def get_groups_supplies(db: Session = Depends(get_db)):
    result = db.query(GroupsHasSupplies).all()
    return result


@groups_supplies.post("", status_code=HTTP_201_CREATED)
def add_group_supply(group_supply: GroupSupplySchema, db: Session = Depends(get_db)):
    db_group = db.query(Groups).filter(Groups.id == group_supply.group_id).first()
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_supply = db.query(Supply).filter(Supply.id == group_supply.supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_group_supply = GroupsHasSupplies(
        group_id=group_supply.group_id,
        supply_id=group_supply.supply_id,
        quantity=group_supply.quantity,
    )
    db.add(new_group_supply)
    db.commit()
    db.refresh(new_group_supply)
    return Response(status_code=HTTP_201_CREATED)


@groups_supplies.put("", response_model=GroupSupplySchema)
def update_quantity(data_update: GroupSupplySchema, db: Session = Depends(get_db)):
    db_relation = (
        db.query(GroupsHasSupplies)
        .filter(
            GroupsHasSupplies.group_id == data_update.group_id,
            GroupsHasSupplies.supply_id == data_update.supply_id,
        )
        .first()
    )
    if not db_relation:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_relation, key, value)
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation
