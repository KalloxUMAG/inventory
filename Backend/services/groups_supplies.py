from sqlalchemy.orm import Session
from models.models import GroupsHasSupplies
from schemas.groups_supplies_schema import GroupSupplySchema
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class GroupSupplyService:
    async def get_groups_supplies(self, db: Session):
        return db.query(GroupsHasSupplies).all()
    async def get_group_supply(self, group_id: int, supply_id: int, db: Session):
        return db.query(GroupsHasSupplies).filter(
            GroupsHasSupplies.group_id == group_id,
            GroupsHasSupplies.supply_id == supply_id,
        ).first()
    async def add_group_supply(self, user_id: int, group_supply: GroupSupplySchema, db: Session):
        new_group_supply = GroupsHasSupplies(
            group_id=group_supply.group_id,
            supply_id=group_supply.supply_id,
            quantity=group_supply.quantity,
        )
        db.add(new_group_supply)
        db.commit()
        db.refresh(new_group_supply)
        return new_group_supply
    async def update_quantity(self, user_id: int, relation: GroupSupplySchema, data_update: GroupSupplySchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(relation, key, value)
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation