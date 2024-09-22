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
from schemas.groups_supplies_schema import GroupSupplySchema
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG
from services.user_group_role import UserGroupRoleService
from services.groups_supplies import GroupSupplyService
from auth.auth_bearer import user_context

permissionsService = UserGroupRoleService()
groupSuppliesService = GroupSupplyService()

class LotService:
    async def get_lots(self, db: Session):
        permissions = await permissionsService.get_user_groups_and_roles(user_context.get(), db)
        groups = [permission[2] for permission in permissions]
        result = (
            db.query(
                Lot.id,
                Lot.number,
                Lot.reception_date,
                Lot.due_date,
                Lot.observations,
                Lot.group_id,
                Lot.stock,
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
            .filter(Lot.group_id.in_(groups))
            .all()
        )
        return result
    async def get_lot_to_loan(self, lot_id:int, db: Session):
        result = db.query(Lot).filter(Lot.id == lot_id).first()
        return  result
    async def get_lot_simple(self, lot_id: int, db: Session):
        permissions = await permissionsService.get_user_groups_and_roles(user_context.get(), db)
        groups = [permission[2] for permission in permissions]
        return db.query(Lot).filter(Lot.id == lot_id, Lot.group_id.in_(groups)).first()
    async def get_lot(self, lot_id: int, db: Session):
        permissions = await permissionsService.get_user_groups_and_roles(user_context.get(), db)
        groups = [permission[2] for permission in permissions]
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
            .filter(Lot.group_id.in_(groups))
            .first()
        )
        return result
    async def get_lots_by_supply(self, supply_id: int, db: Session):
        permissions = await permissionsService.get_user_groups_and_roles(user_context.get(), db)
        groups = [permission[2] for permission in permissions]
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
                Lot.stock,
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
            .filter(Lot.supplies_id == supply_id, Lot.state == True, Lot.group_id.in_(groups))
            .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
            .outerjoin(Location, Location.id == SubLocation.id)
            .outerjoin(Project, Project.id == Lot.project_id)
            .outerjoin(ProjectOwner, ProjectOwner.id == Project.owner_id)
            .outerjoin(Supplier, Supplier.id == Lot.supplier_id)
            .outerjoin(Groups, Groups.id == Lot.group_id)
            .all()
        )
        return result
    
    async def get_lots_by_supply_group(self, supply_id: int, group_id, db: Session):
        permissions = await permissionsService.get_user_groups_and_roles(user_context.get(), db)
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
                Lot.stock,
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
            .filter(Lot.supplies_id == supply_id, Lot.state == True, Lot.stock > 0, Lot.group_id == group_id)
            .outerjoin(SubLocation, SubLocation.id == Lot.sub_location_id)
            .outerjoin(Location, Location.id == SubLocation.id)
            .outerjoin(Project, Project.id == Lot.project_id)
            .outerjoin(ProjectOwner, ProjectOwner.id == Project.owner_id)
            .outerjoin(Supplier, Supplier.id == Lot.supplier_id)
            .outerjoin(Groups, Groups.id == Lot.group_id)
            .all()
        )
        return result
    @log_func_calls("lots", CREATE_LOG)
    async def add_lot(self, user_id: int, lot: CreateLotSchema, db: Session):
        db_supply = db.query(Supply).filter(Supply.id == lot.supply_id).first()
        stock_to_add = db_supply.lot_stock
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
            stock=stock_to_add,
            group_id=lot.group_id,
        )
        db.add(new_lot)
        db.commit()
        db.refresh(new_lot)
        group_supply_db = await groupSuppliesService.get_group_supply(group_id=lot.group_id, supply_id=lot.supply_id, db=db)
        if not group_supply_db:
            group_supply = GroupSupplySchema(
                group_id=lot.group_id,
                supply_id=lot.supply_id,
                quantity=stock_to_add,
            )
            await groupSuppliesService.add_group_supply(user_id, group_supply, db)
        else:
            group_supply = GroupSupplySchema(group_id=lot.group_id, supply_id=lot.supply_id, quantity=group_supply_db.quantity + stock_to_add)
            await groupSuppliesService.update_quantity(user_id=user_id, relation=group_supply_db, data_update=group_supply, db=db)
        new_supply_stock = db_supply.stock + stock_to_add
        setattr(db_supply, "stock", new_supply_stock)
        db.add(db_supply)
        db.commit()
        db.refresh(db_supply)
        return new_lot
    @log_func_calls("lots", UPDATE_LOG)
    async def update_lot(self, user_id: int, lot, data_update: CreateLotSchema, db: Session):
        old_stock = lot.stock
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(lot, key, value)
        db.add(lot)
        db.commit()
        db.refresh(lot)
        new_stock = data_update.stock
        if new_stock != old_stock:
            difference_stock = new_stock - old_stock
            group_supply_db = await groupSuppliesService.get_group_supply(group_id=lot.group_id, supply_id=lot.supplies_id, db=db)
            group_supply = GroupSupplySchema(group_id=lot.group_id, supply_id=lot.supplies_id, quantity=group_supply_db.quantity + new_stock - old_stock)
            await groupSuppliesService.update_quantity(user_id=user_id, relation=group_supply_db, data_update=group_supply, db=db)
            db_supply = db.query(Supply).filter(Supply.id == lot.supplies_id).first()
            new_supply_stock = db_supply.stock + difference_stock
            setattr(db_supply, "stock", new_supply_stock)
            db.add(db_supply)
            db.commit()
            db.refresh(db_supply)
        return lot
    @log_func_calls("lots", DELETE_LOG)
    async def delete_lot(self, user_id: int, lot, db: Session):
        setattr(lot, "state", False)
        db.add(lot)
        db.commit()
        db.refresh(lot)
        group_supply_db = await groupSuppliesService.get_group_supply(group_id=lot.group_id, supply_id=lot.supplies_id, db=db)
        group_supply = GroupSupplySchema(group_id=lot.group_id, supply_id=lot.supplies_id, quantity=group_supply_db.quantity - lot.stock)
        await groupSuppliesService.update_quantity(user_id=user_id, relation=group_supply_db, data_update=group_supply, db=db)
        db_supply = db.query(Supply).filter(Supply.id == lot.supplies_id).first()
        new_supply_stock = db_supply.stock - lot.stock
        setattr(db_supply, "stock", new_supply_stock)
        db.add(db_supply)
        db.commit()
        db.refresh(db_supply)
        return lot