from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Equipments, Suppliers, Invoices, Models, Rooms, Units, Buildings, Maintenances
from schemas.equipment_schema import EquipmentSchema, EquipmentFullSchema, EquipmentListSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

from routes.suppliers import get_supplier
from routes.invoices import get_invoice
from routes.models import get_model
from routes.rooms import get_room

equipments = APIRouter()

@equipments.get("/api/equipments", response_model=List[EquipmentListSchema])
def get_equipments(db:Session = Depends(get_db)):
    result = db.query(
       Equipments.id, Equipments.name, Equipments.serial_number, Equipments.umag_inventory_code, Equipments.reception_date, Equipments.maintenance_period, Equipments.observation,
       Equipments.room_id, Rooms.name.label("room_name"), Equipments.supplier_id, Suppliers.name.label("supplier_name"), Equipments.invoice_id, Invoices.number.label("invoice_number"),
       Equipments.model_id, Models.model.label("model_model")).outerjoin(
       Rooms, Rooms.id == Equipments.room_id).outerjoin(Suppliers, Suppliers.id == Equipments.supplier_id).outerjoin(Invoices, Invoices.id == Equipments.invoice_id).outerjoin(
       Models, Models.id == Equipments.model_id).all()
    return result

@equipments.post("/api/equipments", status_code=HTTP_201_CREATED)
def add_equipment(equipment: EquipmentSchema, db:Session = Depends(get_db)):
   if equipment.supplier_id != None:
      db_supplier = get_supplier(equipment.supplier_id, db=db)
      if not db_supplier:
         return Response(status_code=HTTP_404_NOT_FOUND)
   if equipment.invoice_id != None:
      db_invoice = get_invoice(equipment.invoice_id, db=db)
      if not db_invoice:
         return Response(status_code=HTTP_404_NOT_FOUND)
   if equipment.model_id != None:
      db_model = get_model(equipment.model_id, db=db)
      if not db_model:
         return Response(status_code=HTTP_404_NOT_FOUND)
   if equipment.room_id != None:
      db_room = get_room(equipment.room_id, db=db)
      if not db_room:
         return Response(status_code=HTTP_404_NOT_FOUND)
      
   new_equipment = Equipments(name = equipment.name, serial_number = equipment.serial_number, umag_inventory_code = equipment.umag_inventory_code, reception_date = equipment.reception_date, 
                               maintenance_period = equipment.maintenance_period, observation = equipment.observation, last_preventive_mainteinance = equipment.last_preventive_mainteinance,
                               supplier_id = equipment.supplier_id, invoice_id = equipment.invoice_id, model_id = equipment.model_id, room_id = equipment.room_id)
   db.add(new_equipment)
   db.commit()
   db.refresh(new_equipment)
   content = str(new_equipment.id)
   return Response(status_code=HTTP_201_CREATED, content=content)

@equipments.get("/api/equipments/{equipment_id}", response_model=EquipmentFullSchema)
def get_equipment(equipment_id: int, db:Session = Depends(get_db)):
   result = db.query(
      Equipments.id, Equipments.name, Equipments.serial_number, Equipments.umag_inventory_code, Equipments.reception_date, Equipments.maintenance_period, Equipments.observation,
      Equipments.room_id, Rooms.name.label("room_name"), Equipments.supplier_id, Suppliers.name.label("supplier_name"), Equipments.invoice_id, Invoices.number.label("invoice_number"),
      Equipments.model_id, Models.model.label("model_model"), Units.id.label("unit_id"), Units.name.label("unit_name"), Buildings.id.label("building_id"), Buildings.name.label("building_name")
      ).outerjoin(
      Rooms, Rooms.id == Equipments.room_id).outerjoin(Suppliers, Suppliers.id == Equipments.supplier_id).outerjoin(Invoices, Invoices.id == Equipments.invoice_id).outerjoin(
      Models, Models.id == Equipments.model_id).outerjoin(Units, Units.id == Rooms.unit_id).outerjoin(Buildings, Buildings.id == Units.building_id).filter(Equipments.id == equipment_id).first()
   return result

@equipments.get("/api/equipment/{equipment_id}", response_model=EquipmentSchema)
def get_equipment_exist(equipment_id: int, db:Session = Depends(get_db)):
   return db.query(Equipments).filter(Equipments.id == equipment_id)

@equipments.delete("/api/equipments/{equipment_id}", status_code=HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, db:Session = Depends(get_db)):
    db_equipment = db.query(Equipments).filter(Equipments.id == equipment_id).first()
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_equipment)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)