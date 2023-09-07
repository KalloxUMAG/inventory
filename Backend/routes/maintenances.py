from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from config.database import get_db
from models.models import Maintenance
from routes.equipments import get_equipment_exist
from schemas.maintenance_schema import (
    EditMaintenanceSchema,
    MaintenanceFromEquipment,
    MaintenanceSchema,
)

from auth.auth_bearer import JWTBearer

maintenances = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["equipments"], prefix="/api/maintenances"
)


@maintenances.get("", response_model=List[MaintenanceSchema])
def get_maintenances(db: Session = Depends(get_db)):
    result = db.query(Maintenance).all()
    return result


@maintenances.post("", status_code=HTTP_201_CREATED)
def add_maintenances(maintenance: MaintenanceSchema, db: Session = Depends(get_db)):
    db_equipment = get_equipment_exist(maintenance.equiptment_id, db=db)
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
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
    return Response(status_code=HTTP_201_CREATED)


@maintenances.get("/maintenance/{maintenance_id}", response_model=MaintenanceSchema)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    return db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()


@maintenances.get("/{equipment_id}", response_model=List[MaintenanceFromEquipment])
def get_maintenances_equipment(equipment_id: int, db: Session = Depends(get_db)):
    return (
        db.query(
            Maintenance.id,
            Maintenance.date,
            Maintenance.maintenance_type,
            Maintenance.observations,
            Maintenance.state,
            Maintenance.equiptment_id,
        )
        .filter(Maintenance.equiptment_id == equipment_id)
        .order_by(Maintenance.date.desc())
        .all()
    )


@maintenances.get(
    "/last_maintenance/{equipment_id}",
    response_model=MaintenanceFromEquipment,
)
def get_last_maintenance_equipment(equipment_id: int, db: Session = Depends(get_db)):
    return (
        db.query(
            Maintenance.id,
            Maintenance.date,
            Maintenance.maintenance_type,
            Maintenance.observations,
            Maintenance.state,
            Maintenance.equiptment_id,
        )
        .filter(
            Maintenance.equiptment_id == equipment_id,
            Maintenance.maintenance_type == "Programada",
        )
        .order_by(Maintenance.date.desc())
        .first()
    )


@maintenances.put("/{maintenance_id}", response_model=MaintenanceSchema)
def update_maintenance(
    data_update: EditMaintenanceSchema,
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    db_maintenance = get_maintenance(maintenance_id, db=db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_maintenance, key, value)
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@maintenances.delete("/{maintenance_id}", status_code=HTTP_204_NO_CONTENT)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = get_maintenance(maintenance_id, db=db)
    if not db_maintenance:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_maintenance)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
