import logging
from pathlib import Path
from typing import List
from datetime import datetime, timedelta
import re
import os

from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from config.database import get_db
from config.settings import settings
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
from routes.invoices import get_invoice
from routes.model_numbers import get_model_number
from routes.rooms import get_room
from routes.stages import get_stage
from routes.suppliers import get_supplier
from schemas.equipment_schema import (
    EquipmentFullSchema,
    EquipmentListSchema,
    EquipmentTypeSchema,
    EquipmentSchema,
    CriticEquipmentSchema,
    UpdateEquipmentSchema,
)

from auth.auth_bearer import JWTBearer

equipments = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["equipments"], prefix="/api/equipments"
)


@equipments.get("", response_model=List[EquipmentListSchema])
def get_equipments(db: Session = Depends(get_db)):
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


@equipments.get("/types", response_model=List[EquipmentTypeSchema])
def get_equipment_types(db: Session = Depends(get_db)):
    return db.query(EquipmentTypes).all()


@equipments.post("/types", status_code=HTTP_201_CREATED)
def add_equipment_type(equipment_type: EquipmentTypeSchema, db: Session = Depends(get_db)):
    db_equipment_type = (
        db.query(EquipmentTypes).filter(EquipmentTypes.name == equipment_type.name).first()
    )
    if db_equipment_type:
        return Response(status_code=HTTP_409_CONFLICT)
    new_equipment_type = EquipmentTypes(name=equipment_type.name)
    db.add(new_equipment_type)
    db.commit()
    db.refresh(new_equipment_type)
    content = str(new_equipment_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@equipments.get("/nextmaintenances", response_model=List[CriticEquipmentSchema])
def get_equipments_nextmaintenances(db: Session = Depends(get_db)):
    s = text(
        """ SELECT "Equipments".*, "Rooms".id as room_id, "Rooms".name as room_name FROM "Equipments", "Rooms" WHERE "Equipments".next_maintenance <= (CURRENT_DATE + interval '8 month') AND "Rooms".id = "Equipments".room_id;"""
    )
    query = db.execute(s).all()
    return query


@equipments.post("", status_code=HTTP_201_CREATED)
def add_equipment(equipment: EquipmentSchema, db: Session = Depends(get_db)):
    if equipment.supplier_id is not None:
        db_supplier = get_supplier(equipment.supplier_id, db=db)
        if not db_supplier:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.invoice_id is not None:
        db_invoice = get_invoice(equipment.invoice_id, db=db)
        if not db_invoice:
            logging.warning("No se encontro el invoice", equipment.invoice_id)
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.model_number_id is not None:
        db_model_number = get_model_number(equipment.model_number_id, db=db)
        if not db_model_number:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.room_id is not None:
        db_room = get_room(equipment.room_id, db=db)
        if not db_room:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.stage_id is not None:
        db_stage = get_stage(equipment.stage_id, db=db)
        if not db_stage:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.equipment_type_id is not None:
        db_equipment_type = (
            db.query(EquipmentTypes)
            .filter(EquipmentTypes.id == equipment.equipment_type_id)
            .first()
        )
        if not db_equipment_type:
            return Response(status_code=HTTP_404_NOT_FOUND)

    if equipment.maintenance_period != None:
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
    content = str(new_equipment.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


# Upload image to equipments folder using invoice id
@equipments.post("/{equipment_id}", status_code=HTTP_201_CREATED)
async def add_image(equipment_id: int, file: UploadFile):
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
    return Response(status_code=HTTP_201_CREATED)


# Get images from equipments folder
@equipments.get("/image/{equipment_id}")
async def get_images(equipment_id: int):
    image_path = Path(settings.image_directory, "equipments", str(equipment_id))
    if not image_path.exists():
        return Response(status_code=HTTP_404_NOT_FOUND)

    image_base_url = settings.base_url.path.replace("/api", "/images")
    return [
        {
            "id": i,
            "name": file.name,
            "path": f"{image_base_url}/equipments/{equipment_id}/{file.name}",
        }
        for i, file in enumerate(image_path.iterdir(), start=1)
    ]


@equipments.get("/{equipment_id}", response_model=EquipmentFullSchema)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
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


@equipments.get("/equipment/{equipment_id}", response_model=EquipmentSchema)
def get_equipment_exist(equipment_id: int, db: Session = Depends(get_db)):
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()


@equipments.delete("/{equipment_id}", status_code=HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_equipment)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@equipments.put("/{equipment_id}", status_code=HTTP_200_OK)
def update_equipment(
    data_update: UpdateEquipmentSchema, equipment_id: int, db: Session = Depends(get_db)
):
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=False).items():
        if value is not None:
            setattr(db_equipment, key, value)
        else:
            setattr(db_equipment, key, None)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    content = str(db_equipment.id)
    return Response(status_code=HTTP_200_OK, content=content)


# Delete images equipments folder
@equipments.delete("/image/{equipment_id}", status_code=HTTP_200_OK)
async def delete_image(equipment_id: int, file: UploadFile):
    image_path = Path(settings.image_directory, "equipments", str(equipment_id))
    image_path.mkdir(parents=True, exist_ok=True)
    extension = file.filename.split(".")[-1].lower()
    format_filename = file.filename[: -len(extension)].lower()
    format_filename = re.sub("[^A-Za-z0-9_]", "", format_filename, 0, re.IGNORECASE)
    os.remove(str(image_path) + "/" + str(format_filename) + "." + str(extension))
    return Response(status_code=HTTP_200_OK)
