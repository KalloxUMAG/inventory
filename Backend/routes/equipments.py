import logging
from pathlib import Path
from typing import List
from datetime import datetime
import re
import os

from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from config.database import get_db
from services.equipments import EquipmentService
from services.suppliers import SupplierService
from services.invoices import InvoiceService
from services.model_numbers import ModelNumberService
from services.rooms import RoomService
from services.stages import StageService

from config.settings import settings
from models.models import (
    Equipment,
)
from routes.stages import get_stage
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
service = EquipmentService()
supplier_service = SupplierService()
invoice_service = InvoiceService()
model_number_service = ModelNumberService()
room_service = RoomService()
stage_service = StageService()

@equipments.get("", response_model=List[EquipmentListSchema])
async def get_equipments(db: Session = Depends(get_db)):
    equipments = await service.get_equipments(db)
    return equipments


@equipments.get("/types", response_model=List[EquipmentTypeSchema])
async def get_equipment_types(db: Session = Depends(get_db)):
    equipments_types = await service.get_equipment_types(db)
    return equipments_types


@equipments.post("/types", status_code=HTTP_201_CREATED)
async def add_equipment_type(equipment_type: EquipmentTypeSchema, db: Session = Depends(get_db)):
    db_equipment_type = await service.get_equipment_type_by_name(equipment_type.name, db=db)
    if db_equipment_type:
        return Response(status_code=HTTP_409_CONFLICT)
    new_equipment_type = await service.add_equipment_type(equipment_type, db=db)
    content = str(new_equipment_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@equipments.get("/nextmaintenances", response_model=List[CriticEquipmentSchema])
async def get_equipments_nextmaintenances(db: Session = Depends(get_db)):
    next_maintenances = await service.get_equipments_next_maintenances(db)
    return next_maintenances


@equipments.post("", status_code=HTTP_201_CREATED)
async def add_equipment(equipment: EquipmentSchema, db: Session = Depends(get_db)):
    if equipment.supplier_id is not None:
        db_supplier = await supplier_service.get_supplier(equipment.supplier_id, db=db)
        if not db_supplier:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.invoice_id is not None:
        db_invoice = await invoice_service.get_invoice(equipment.invoice_id, db=db)
        if not db_invoice:
            logging.warning("No se encontro el invoice", equipment.invoice_id)
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.model_number_id is not None:
        db_model_number = await model_number_service.get_model_number(equipment.model_number_id, db=db)
        if not db_model_number:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.room_id is not None:
        db_room = await room_service.get_room(equipment.room_id, db=db)
        if not db_room:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.stage_id is not None:
        db_stage = await get_stage(equipment.stage_id, db=db)
        if not db_stage:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.equipment_type_id is not None:
        db_equipment_type = await service.get_equipment_type(equipment.equipment_type_id, db=db
        )
        if not db_equipment_type:
            return Response(status_code=HTTP_404_NOT_FOUND)

    new_equipment = await service.add_equipment(equipment, db=db)
    content = str(new_equipment.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


# Upload image to equipments folder using invoice id
@equipments.post("/{equipment_id}", status_code=HTTP_201_CREATED)
async def add_image(equipment_id: int, file: UploadFile):
    await service.add_image(equipment_id, file)
    return Response(status_code=HTTP_201_CREATED)


# Get images from equipments folder
@equipments.get("/image/{equipment_id}")
async def get_images(equipment_id: int):
    images = await service.get_images(equipment_id)
    return images


@equipments.get("/{equipment_id}", response_model=EquipmentFullSchema)
async def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = await service.get_equipment(equipment_id, db)
    return equipment


@equipments.get("/equipment/{equipment_id}", response_model=EquipmentSchema)
async def get_equipment_exist(equipment_id: int, db: Session = Depends(get_db)):
    equipment = await service.get_equipment_simple(equipment_id, db)
    return equipment


@equipments.delete("/{equipment_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = await service.get_equipment_simple(equipment_id, db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_equipment(db_equipment, db)
    return Response(status_code=HTTP_204_NO_CONTENT)


@equipments.put("/{equipment_id}", status_code=HTTP_200_OK)
async def update_equipment(
    data_update: UpdateEquipmentSchema, equipment_id: int, db: Session = Depends(get_db)
):
    db_equipment = await service.get_equipment_simple(equipment_id, db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_equipment = await service.update_equipment(db_equipment, data_update, db)
    content = str(update_equipment.id)
    return Response(status_code=HTTP_200_OK, content=content)


# Delete images equipments folder
@equipments.delete("/image/{equipment_id}", status_code=HTTP_200_OK)
async def delete_image(equipment_id: int, file: UploadFile):
    await service.delete_image(equipment_id, file)
    return Response(status_code=HTTP_200_OK)
