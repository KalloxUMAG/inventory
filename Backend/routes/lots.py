from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.lots import LotService
from models.models import Lot
from schemas.lot_schema import CreateLotSchema, LotListSchema

from auth.auth_bearer import JWTBearer

lots = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["supplies"], prefix="/api/lots"
)
service = LotService()


@lots.get("", response_model=List[LotListSchema])
async def get_lots(db: Session = Depends(get_db)):
    lots = await service.get_lots(db)
    return lots


@lots.post("", status_code=HTTP_201_CREATED)
async def add_lots(lot: CreateLotSchema, db: Session = Depends(get_db)):
    new_lot = await service.add_lot(lot, db)
    content = str(new_lot.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@lots.get("/lot/{lot_id}", response_model=LotListSchema)
async def get_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = await service.get_lot(lot_id, db)
    if not lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return lot


@lots.get("/supply/{supply_id}", response_model=List[LotListSchema])
async def get_lots_supply(supply_id: int, db: Session = Depends(get_db)):
    lots = await service.get_lots_by_supply(supply_id, db)
    return lots


@lots.put("/{lot_id}", response_model=CreateLotSchema)
async def update_lot(
    data_update: CreateLotSchema, lot_id: int, db: Session = Depends(get_db)
):
    db_lot = await service.get_lot_simple(lot_id, db)
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    updated_lot = await service.update_lot(data_update, db_lot, db)
    return updated_lot


@lots.put("/deactive/{lot_id}", status_code=HTTP_205_RESET_CONTENT)
async def deactive_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = await service.get_lot_simple(lot_id, db)
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    deactivated_lot = await service.delete_lot(db_lot, db)
    return Response(status_code=HTTP_205_RESET_CONTENT)
