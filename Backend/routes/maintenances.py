from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from services.maintenances import MaintenanceService
from services.equipments import EquipmentService
from schemas.maintenance_schema import (
    EditMaintenanceSchema,
    MaintenanceFromEquipment,
    MaintenanceSchema,
)


from auth.auth_bearer import JWTBearer, get_user_id_from_token

maintenances = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["equipments"], prefix="/api/maintenances"
)
service = MaintenanceService()
equipment_service = EquipmentService()

@maintenances.get("", response_model=List[MaintenanceSchema])
async def get_maintenances(db: Session = Depends(get_db)):
    maintenances = await service.get_maintenances(db)
    return maintenances


@maintenances.post("", status_code=HTTP_201_CREATED)
async def add_maintenances(maintenance: MaintenanceSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_equipment = await equipment_service.get_equipment_simple(maintenance.equiptment_id, db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_maintenance = await service.add_maintenance(user_id=get_user_id_from_token(dependencies), maintenance=maintenance, equipment=db_equipment, db=db)
    return Response(status_code=HTTP_201_CREATED)


@maintenances.get("/maintenance/{maintenance_id}", response_model=MaintenanceSchema)
async def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = await service.get_maintenance(maintenance_id, db)
    if not maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return maintenance

@maintenances.get("/{equipment_id}", response_model=List[MaintenanceFromEquipment])
async def get_maintenances_equipment(equipment_id: int, db: Session = Depends(get_db)):
    maintenances = await service.get_maintenances_by_equipment(equipment_id, db)
    return maintenances


@maintenances.get(
    "/last_maintenance/{equipment_id}",
    response_model=MaintenanceFromEquipment,
)
async def get_last_maintenance_equipment(equipment_id: int, db: Session = Depends(get_db)):
    maintenance = await service.get_last_maintenance_equipment(equipment_id, db)
    if not maintenance:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return maintenance


@maintenances.put("/{maintenance_id}", response_model=MaintenanceSchema)
async def update_maintenance(
    data_update: EditMaintenanceSchema,
    maintenance_id: int,
    dependencies=Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    db_maintenance = get_maintenance(maintenance_id, db=db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    maintenance = await service.update_maintenance(user_id=get_user_id_from_token(dependencies), maintenance=db_maintenance, data_update=data_update, db=db)
    return maintenance


@maintenances.delete("/{maintenance_id}", status_code=HTTP_200_OK)
async def delete_maintenance(maintenance_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_maintenance = await service.get_maintenance(maintenance_id, db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_maintenance(user_id=get_user_id_from_token(dependencies), maintenance=db_maintenance, db=db)
    return Response(status_code=HTTP_200_OK)
