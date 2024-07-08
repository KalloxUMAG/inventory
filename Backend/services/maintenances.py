from datetime import timedelta
from sqlalchemy.orm import Session
from models.models import Maintenance
from schemas.maintenance_schema import MaintenanceSchema

from services.equipments import EquipmentService
equipment_service = EquipmentService()

from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class MaintenanceService:
    async def get_maintenances(self, db: Session):
        return db.query(Maintenance).all()
    async def get_maintenance(self, maintenance_id: int, db: Session):
        return db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    async def get_maintenances_by_equipment(self, equipment_id: int, db: Session):
        return db.query(Maintenance).filter(Maintenance.equiptment_id == equipment_id).order_by(Maintenance.date.desc()).all()
    async def get_last_maintenance_equipment(self, equipment_id: int, db: Session):
        return db.query(Maintenance).filter(Maintenance.equiptment_id == equipment_id, Maintenance.maintenance_type == "Programada").order_by(Maintenance.date.desc()).first()
    @log_func_calls("maintenances", CREATE_LOG)
    async def add_maintenance(self, user_id: int, maintenance: MaintenanceSchema, equipment, db: Session):
        new_maintenance = Maintenance(
            date=maintenance.date,
            observations=maintenance.observations,
            state=maintenance.state,
            maintenance_type=maintenance.maintenance_type,
            equiptment_id=maintenance.equiptment_id,
        )
        db.add(new_maintenance)
        db.commit()
        db.refresh(new_maintenance)
        if maintenance.maintenance_type == "Correctiva":
            return new_maintenance
        last_maintenance = await self.get_last_maintenance_equipment(maintenance.equiptment_id, db)
        if last_maintenance.id == new_maintenance.id:
            next_maintenance = last_maintenance.date + timedelta(
                days=equipment.maintenance_period * 30
            )
            setattr(equipment, "next_maintenance", next_maintenance)
            db.add(equipment)
            db.commit()
            db.refresh(equipment)
        return new_maintenance
    async def update_maintenance(self, user_id: int, maintenance: MaintenanceSchema, data_update, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(maintenance, key, value)
        db.add(maintenance)
        db.commit()
        db.refresh(maintenance)
        if maintenance.maintenance_type == "Correctiva":
            return maintenance
        last_maintenance = await self.get_last_maintenance_equipment(maintenance.equiptment_id, db)
        if last_maintenance.id == maintenance.id:
            db_equipment = await equipment_service.get_equipment_exist(maintenance.equiptment_id, db)
            next_maintenance = last_maintenance.date + timedelta(
                days=db_equipment.maintenance_period * 30
            )
            setattr(db_equipment, "next_maintenance", next_maintenance)
            db.add(db_equipment)
            db.commit()
            db.refresh(db_equipment)
        return maintenance
    async def delete_maintenance(self, user_id: int, maintenance: MaintenanceSchema, db: Session):
        db.delete(maintenance)
        db.commit()
        return maintenance