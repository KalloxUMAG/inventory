from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Supply, SupplyBrand, SupplyFormat, SupplyType
from schemas.supply_schema import (
    SupplyListSchema,
    SupplySchema,
    SupplySchemaFull,
    UpdateStockSchema,
)
from services.lots import LotService
lot_service = LotService()

class SupplyService:
    async def get_supplies(self, db: Session):
        results_db = (
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
                SupplyBrand.id.label("supplies_brand_id"),
                SupplyBrand.name.label("supplies_brand_name"),
                SupplyType.id.label("supplies_type_id"),
                SupplyType.name.label("supplies_type_name"),
                SupplyFormat.id.label("supplies_format_id"),
                SupplyFormat.name.label("supplies_format_name"),
            )
            .outerjoin(SupplyBrand, SupplyBrand.id == Supply.supplies_brand_id)
            .outerjoin(SupplyType, SupplyType.id == Supply.supplies_type_id)
            .outerjoin(SupplyFormat, SupplyFormat.id == Supply.supplies_format_id)
            .filter(Supply.state == True)
            .all()
        )

        # Append lots to supplies
        results = [
            SupplyListSchema(
                id = result.id,
                name = result.name,
                code = result.code,
                state = result.state,
                stock = result.stock,
                lot_stock = result.lot_stock,
                samples = result.samples,
                critical_stock = result.critical_stock,
                observation = result.observation,
                supplies_brand_id = result.supplies_brand_id,
                supplies_brand_name = result.supplies_brand_name,
                supplies_type_id = result.supplies_type_id,
                supplies_type_name = result.supplies_type_name,
                supplies_format_id = result.supplies_format_id,
                supplies_format_name = result.supplies_format_name,
                lots = await lot_service.get_lots_by_supply(result.id, db)
                ) for result in results_db]
        return results
    
    async def get_supply(self, supply_id: int, db: Session):
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
            .filter(and_(Supply.id == supply_id, Supply.state == True))
            .outerjoin(SupplyBrand, SupplyBrand.id == Supply.supplies_brand_id)
            .outerjoin(SupplyType, SupplyType.id == Supply.supplies_type_id)
            .outerjoin(SupplyFormat, SupplyFormat.id == Supply.supplies_format_id)
            .first()
        )
        return result
    async def get_supplies_critical(self, db: Session):
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
            .filter(and_(Supply.stock <= Supply.critical_stock, Supply.state == True))
            .all()
        )
        return result
    async def add_supply(self, supply: SupplySchema, db: Session):
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
        return new_supply
    async def update_stock(self, supply: SupplySchema, data_update: SupplySchema, db: Session):
        setattr(supply, "stock", supply.stock + data_update.stock)
        db.add(supply)
        db.commit()
        db.refresh(supply)
        return supply
    async def update_supply(self, supply: SupplySchema, data_update: SupplySchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(supply, key, value)
        db.add(supply)
        db.commit()
        db.refresh(supply)
        return supply
    async def delete_supply(self, supply: SupplySchema, db: Session):
        setattr(supply, "state", False)
        db.add(supply)
        db.commit()
        db.refresh(supply)
        return supply