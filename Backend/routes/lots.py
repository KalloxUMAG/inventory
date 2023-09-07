from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import (
    Location,
    Lot,
    Project,
    ProjectOwner,
    SubLocation,
    Supplier,
    Supply,
)
from schemas.lot_schema import CreateLotSchema, LotListSchema

from auth.auth_bearer import JWTBearer

lots = APIRouter(dependencies=[Depends(JWTBearer())], tags=["supplies"])


@lots.get("/api/lots", response_model=List[LotListSchema])
def get_lots(db: Session = Depends(get_db)):
    result = (
        db.query(
            Lot.id,
            Lot.number,
            Lot.due_date,
            Lot.observations,
            Supply.name.label("supply_name"),
            Supply.code.label("supply_code"),
            Location.name.label("location"),
            SubLocation.name.label("sub_location"),
            Project.name.label("project"),
        )
        .outerjoin(Supply, Supply.id == Lot.supplies_id)
        .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
        .outerjoin(Location, Location.id == SubLocation.id)
        .outerjoin(Project, Project.id == Lot.project_id)
        .all()
    )
    return result


@lots.post("/api/lots", status_code=HTTP_201_CREATED)
def add_lots(lot: CreateLotSchema, db: Session = Depends(get_db)):
    new_lot = lot(
        number=lot.number,
        due_date=lot.due_date,
        observations=lot.observations,
        supplies_id=lot.supply_id,
        sub_location_id=lot.sub_location_id,
        project_id=lot.project_id,
        supplier_id=lot.supplier_id,
        state=True,
    )
    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)
    content = str(new_lot.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@lots.get("/api/lots/lot/{lot_id}", response_model=LotListSchema)
def get_lot(lot_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Lot.id,
            Lot.number,
            Lot.due_date,
            Lot.observations,
            Supply.name.label("supply_name"),
            Supply.code.label("supply_code"),
            Supply.cost.label("supply_cost"),
            Location.name.label("location"),
            SubLocation.name.label("sub_location"),
            Project.name.label("project"),
            Supplier.name.label("supplier_name"),
        )
        .filter(Lot.id == lot_id and Lot.state is True)
        .outerjoin(Supply, Supply.id == Lot.supplies_id)
        .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
        .outerjoin(Location, Location.id == SubLocation.id)
        .outerjoin(Project, Project.id == Lot.project_id)
        .outerjoin(Supplier, Supplier.id == Supply.supplier_id)
        .first()
    )
    return result


@lots.get("/api/lots/supply/{supply_id}", response_model=List[LotListSchema])
def get_lots_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Lot.id,
            Lot.number,
            Lot.due_date,
            Lot.observations,
            Location.id.label("location_id"),
            Location.name.label("location"),
            Lot.sub_location_id,
            SubLocation.name.label("sub_location"),
            Lot.project_id,
            Project.name.label("project"),
            ProjectOwner.id.label("project_owner_id"),
            ProjectOwner.name.label("project_owner_name"),
            Lot.supplier_id,
            Supplier.name.label("supplier_name"),
        )
        .filter(Lot.supplies_id == supply_id, Lot.state is True)
        .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
        .outerjoin(Location, Location.id == SubLocation.id)
        .outerjoin(Project, Project.id == Lot.project_id)
        .outerjoin(ProjectOwner, ProjectOwner.id == Project.owner_id)
        .outerjoin(Supplier, Supplier.id == Lot.supplier_id)
        .all()
    )
    return result


@lots.put("/api/lots/{lot_id}", response_model=CreateLotSchema)
def update_lot(
    data_update: CreateLotSchema, lot_id: int, db: Session = Depends(get_db)
):
    db_lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_lot, key, value)
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot


@lots.put("/api/lots/deactive/{lot_id}", status_code=HTTP_205_RESET_CONTENT)
def deactive_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_lot, "state", False)
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return Response(status_code=HTTP_205_RESET_CONTENT)
