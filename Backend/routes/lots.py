from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.lots import LotService
from schemas.lot_schema import CreateLotSchema, LotListSchema

from auth.auth_bearer import JWTBearer, get_user_id_from_token, user_context

from services.user_group_role import UserGroupRoleService

lots = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["supplies"], prefix="/api/lots"
)
service = LotService()
permissionsService = UserGroupRoleService()


@lots.get("", response_model=List[LotListSchema])
async def get_lots(db: Session = Depends(get_db)):
    lots = await service.get_lots(db)
    return lots


@lots.post("", status_code=HTTP_201_CREATED)
async def add_lots(lot: CreateLotSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    permissions = await permissionsService.get_user_group_roles(user_context.get(), lot.group_id, db)
    if not permissions:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User is not in the group")
    if not permissions[3]:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User does not have permission to create lots")
    new_lot = await service.add_lot(user_id=get_user_id_from_token(dependencies), lot=lot, db=db)
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
    data_update: CreateLotSchema, lot_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    permissions = await permissionsService.get_user_group_roles(user_context.get(), data_update.group_id, db)
    if not permissions:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User is not in the group")
    if not permissions[5]:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User does not have permission to edit lots")
    db_lot = await service.get_lot_simple(lot_id, db)
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    updated_lot = await service.update_lot(user_id=get_user_id_from_token(dependencies), lot=db_lot, data_update=data_update, db=db)
    return updated_lot


@lots.put("/deactive/{lot_id}", status_code=HTTP_205_RESET_CONTENT)
async def deactive_lot(lot_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_lot = await service.get_lot_simple(lot_id, db)
    permissions = await permissionsService.get_user_group_roles(user_context.get(), db_lot.group_id, db)
    if not permissions:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User is not in the group")
    if not permissions[6]:
        return Response(status_code=HTTP_401_UNAUTHORIZED, content="User does not have permission to delete lots")
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    deactivated_lot = await service.delete_lot(user_id=get_user_id_from_token(dependencies), lot=db_lot, db=db)
    return Response(status_code=HTTP_205_RESET_CONTENT)
