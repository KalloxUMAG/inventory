from sqlalchemy.orm import Session
from models.models import (
    Groups,
    GroupsHasSupplies,
    Location,
    Lot,
    Project,
    ProjectOwner,
    SubLocation,
    Supplier,
    Supply
)
from schemas.lot_schema import CreateLotSchema, LotListSchema

class LotService:
    async def get_lots(self, db: Session):
        result = (
            db.query(
                Lot.id,
                Lot.number,
                Lot.reception_date,
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
    async def get_lot_simple(self, lot_id: int, db: Session):
        return db.query(Lot).filter(Lot.id == lot_id).first()
    async def get_lot(self, lot_id: int, db: Session):
        result = (
            db.query(
                Lot.id,
                Lot.number,
                Lot.reception_date,
                Lot.due_date,
                Lot.observations,
                Supply.name.label("supply_name"),
                Supply.code.label("supply_code"),
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
            .outerjoin(Supplier, Supplier.id == Lot.supplier_id)
            .first()
        )
        return result
    async def get_lots_by_supply(self, supply_id: int, db: Session):
        result = (
            db.query(
                Lot.id,
                Lot.number,
                Lot.reception_date,
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
                Lot.group_id,
                Groups.name.label("group_name"),
            )
            .filter(Lot.supplies_id == supply_id, Lot.state == True)
            .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
            .outerjoin(Location, Location.id == SubLocation.id)
            .outerjoin(Project, Project.id == Lot.project_id)
            .outerjoin(ProjectOwner, ProjectOwner.id == Project.owner_id)
            .outerjoin(Supplier, Supplier.id == Lot.supplier_id)
            .outerjoin(Groups, Groups.id == Lot.group_id)
            .all()
        )
        return result
    async def add_lot(self, lot: CreateLotSchema, db: Session):
        new_lot = Lot(
            number=lot.number,
            reception_date=lot.reception_date,
            due_date=lot.due_date,
            observations=lot.observations,
            supplies_id=lot.supply_id,
            sub_location_id=lot.sub_location_id,
            project_id=lot.project_id,
            supplier_id=lot.supplier_id,
            state=True,
            group_id=lot.group_id,
        )
        db.add(new_lot)
        db.commit()
        db.refresh(new_lot)
        return new_lot
    async def update_lot(self, lot, data_update: CreateLotSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(lot, key, value)
        db.add(lot)
        db.commit()
        db.refresh(lot)
        return lot
    async def delete_lot(self, lot, db: Session):
        setattr(lot, "state", False)
        db.add(lot)
        db.commit()
        db.refresh(lot)
        return lot