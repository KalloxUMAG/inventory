import re
import os

from pathlib import Path
from config.settings import settings
from datetime import timedelta, datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.models import (
    Brand,
    Building,
    Equipment,
    EquipmentTypes,
    Invoice,
    Model,
    ModelNumber,
    Project,
    ProjectOwner,
    Room,
    Stage,
    Supplier,
    Unit,
)
from schemas.basic_option_schema import BasicOptionSchema, BasicOptionSchemaWithId
from schemas.equipment_schema import EquipmentSchema, UpdateEquipmentSchema
from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class EquipmentService:
    async def get_equipments(self, db: Session):
        result = (
            db.query(
                Equipment.id,
                Equipment.name,
                Equipment.serial_number,
                Equipment.umag_inventory_code,
                Equipment.reception_date,
                Equipment.maintenance_period,
                Equipment.observation,
                Equipment.room_id,
                Room.name.label("room_name"),
                Equipment.supplier_id,
                Supplier.name.label("supplier_name"),
                Equipment.invoice_id,
                Invoice.number.label("invoice_number"),
                Equipment.model_number_id,
                ModelNumber.number.label("model_number"),
                Model.id.label("model_id"),
                Model.name.label("model_name"),
                Equipment.stage_id,
                Stage.name.label("stage_name"),
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                EquipmentTypes.id.label("equipment_type_id"),
                EquipmentTypes.name.label("equipment_type_name"),
            )
            .outerjoin(Room, Room.id == Equipment.room_id)
            .outerjoin(Supplier, Supplier.id == Equipment.supplier_id)
            .outerjoin(Invoice, Invoice.id == Equipment.invoice_id)
            .outerjoin(ModelNumber, ModelNumber.id == Equipment.model_number_id)
            .outerjoin(Model, Model.id == ModelNumber.model_id)
            .outerjoin(Stage, Stage.id == Equipment.stage_id)
            .outerjoin(Project, Project.id == Stage.project_id)
            .outerjoin(EquipmentTypes, EquipmentTypes.id == Equipment.equipment_type_id)
            .all()
        )
        return result
    async def get_equipment(self, equipment_id: int, db: Session):
        result = (
            db.query(
                Equipment.id,
                Equipment.name,
                Equipment.serial_number,
                Equipment.umag_inventory_code,
                Equipment.reception_date,
                Equipment.maintenance_period,
                Equipment.observation,
                Equipment.last_preventive_mainteinance,
                Equipment.room_id,
                Room.name.label("room_name"),
                Equipment.supplier_id,
                Supplier.name.label("supplier_name"),
                Equipment.invoice_id,
                Invoice.number.label("invoice_number"),
                Brand.id.label("brand_id"),
                Brand.name.label("brand_name"),
                Model.id.label("model_id"),
                Model.name.label("model_name"),
                Equipment.model_number_id,
                ModelNumber.number.label("model_number"),
                Unit.id.label("unit_id"),
                Unit.name.label("unit_name"),
                Building.id.label("building_id"),
                Building.name.label("building_name"),
                Stage.id.label("stage_id"),
                Stage.name.label("stage_name"),
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                ProjectOwner.id.label("project_owner_id"),
                ProjectOwner.name.label("project_owner_name"),
                EquipmentTypes.id.label("equipment_type_id"),
                EquipmentTypes.name.label("equipment_type_name"),
            )
            .outerjoin(Room, Room.id == Equipment.room_id)
            .outerjoin(Supplier, Supplier.id == Equipment.supplier_id)
            .outerjoin(Invoice, Invoice.id == Equipment.invoice_id)
            .outerjoin(ModelNumber, ModelNumber.id == Equipment.model_number_id)
            .outerjoin(Model, Model.id == ModelNumber.id)
            .outerjoin(Brand, Brand.id == Model.brand_id)
            .outerjoin(Unit, Unit.id == Room.unit_id)
            .outerjoin(Building, Building.id == Unit.building_id)
            .outerjoin(Stage, Stage.id == Equipment.stage_id)
            .outerjoin(Project, Project.id == Stage.project_id)
            .outerjoin(ProjectOwner, ProjectOwner.id == Project.owner_id)
            .outerjoin(EquipmentTypes, EquipmentTypes.id == Equipment.equipment_type_id)
            .filter(Equipment.id == equipment_id)
            .first()
        )
        return result
    async def get_equipment_simple(self, equipment_id: int, db: Session):
        return db.query(Equipment).filter(Equipment.id == equipment_id).first()
    async def get_equipment_types(self, db: Session):
        return db.query(EquipmentTypes).all()
    async def get_equipment_type(self, equipment_type_id: int, db: Session):
        return db.query(EquipmentTypes).filter(EquipmentTypes.id == equipment_type_id).first()
    async def get_equipment_type_by_name(self, equipment_type_name: str, db: Session):
        return db.query(EquipmentTypes).filter(EquipmentTypes.name == equipment_type_name).first()
    @log_func_calls("equipment_types", CREATE_LOG)
    async def add_equipment_type(self, user_id: int, equipment_type: BasicOptionSchema, db: Session):
        new_equipment_type = EquipmentTypes(name=equipment_type.name)
        db.add(new_equipment_type)
        db.commit()
        db.refresh(new_equipment_type)
        return new_equipment_type
    async def get_equipments_next_maintenances(self, db: Session):
        s = text(
            """ SELECT "Equipments".*, "Rooms".id as room_id, "Rooms".name as room_name FROM "Equipments", "Rooms" WHERE "Equipments".next_maintenance <= (CURRENT_DATE + interval '8 month') AND "Rooms".id = "Equipments".room_id;"""
        )
        query = db.execute(s).all()
        return query
    @log_func_calls("equipments", CREATE_LOG)
    async def add_equipment(self, user_id: int, equipment: EquipmentSchema, db: Session):
        if equipment.maintenance_period != None:
            print(user_id)
            reception_date = equipment.reception_date
            next_maintenance = reception_date + timedelta(days=equipment.maintenance_period * 30)
            next_maintenance = next_maintenance.strftime("%Y-%m-%d")
        else:
            next_maintenance = None

        new_equipment = Equipment(
            name=equipment.name,
            serial_number=equipment.serial_number,
            umag_inventory_code=equipment.umag_inventory_code,
            reception_date=equipment.reception_date,
            maintenance_period=equipment.maintenance_period,
            observation=equipment.observation,
            last_preventive_mainteinance=equipment.last_preventive_mainteinance,
            next_maintenance=next_maintenance,
            supplier_id=equipment.supplier_id,
            invoice_id=equipment.invoice_id,
            model_number_id=equipment.model_number_id,
            room_id=equipment.room_id,
            stage_id=equipment.stage_id,
            equipment_type_id=equipment.equipment_type_id,
        )
        db.add(new_equipment)
        db.commit()
        db.refresh(new_equipment)
        return new_equipment
    @log_func_calls("equipments", UPDATE_LOG)
    async def update_equipment(self, user_id: int, equipment: EquipmentSchema, data_update: UpdateEquipmentSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            if value is not None:
                print(key, value)
                setattr(equipment, key, value)
            else:
                setattr(equipment, key, None)
        db.add(equipment)
        db.commit()
        db.refresh(equipment)
        return equipment
    @log_func_calls("equipments", DELETE_LOG)
    async def delete_equipment(self, user_id: int, equipment: EquipmentSchema, db: Session):
        db.delete(equipment)
        db.commit()
        return equipment
    async def get_images(self, equipment_id: int):
        image_path = Path(settings.image_directory, "equipments", str(equipment_id))
        if not image_path.exists():
            return []

        image_base_url = settings.base_url.path.replace("/api", "/images")
        return [
            {
                "id": i,
                "name": file.name,
                "path": f"{image_base_url}/equipments/{equipment_id}/{file.name}",
            }
            for i, file in enumerate(image_path.iterdir(), start=1)
        ]
    @log_func_calls("equipment image", CREATE_LOG)
    async def add_image(self, user_id: int, equipment_id: int, file):
        image_path = Path(settings.image_directory, "equipments", str(equipment_id))
        image_path.mkdir(parents=True, exist_ok=True)
        extension = file.filename.split(".")[-1].lower()
        format_filename = file.filename[: -len(extension)].lower()
        format_filename = re.sub("[^A-Za-z0-9]", "", format_filename, 0, re.IGNORECASE)
        date_now = datetime.now()
        date_now = date_now.strftime("%d%m%Y_%H%M%S")
        with open(
            str(image_path) + "/" + str(date_now) + str(format_filename) + "." + str(extension),
            "wb",
        ) as buffer:
            buffer.write(await file.read())
    @log_func_calls("equipment image", DELETE_LOG)
    async def delete_image(self, user_id: int, equipment_id: int, file):
        image_path = Path(settings.image_directory, "equipments", str(equipment_id))
        image_path.mkdir(parents=True, exist_ok=True)
        extension = file.filename.split(".")[-1].lower()
        format_filename = file.filename[: -len(extension)].lower()
        format_filename = re.sub("[^A-Za-z0-9_]", "", format_filename, 0, re.IGNORECASE)
        os.remove(str(image_path) + "/" + str(format_filename) + "." + str(extension))