from typing import List
from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.groups import GroupService
from schemas.group_schema import CreateGroupSchema, GroupSchema

from auth.auth_bearer import JWTBearer, get_user_id_from_token
from dependencies.permissions import check_permissions_factory

groups = APIRouter(
    dependencies=[Depends(JWTBearer()), Depends(check_permissions_factory('grupos'))], tags=["groups"], prefix="/api/groups"
)
service = GroupService()


@groups.get("", response_model=List[GroupSchema])
async def get_groups(db: Session = Depends(get_db)):
    groups = await service.get_groups(db)
    return groups

@groups.get("/{group_id}", response_model=GroupSchema)
async def get_group(group_id: int, db: Session = Depends(get_db)):
    group = await service.get_group(group_id, db)
    if not group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return group
  
@groups.post("", status_code=HTTP_201_CREATED)
async def add_groups(group: CreateGroupSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_group = await service.get_group_by_name(group.name, db)
    if db_group:
        return Response(status_code=HTTP_409_CONFLICT, content="Group already exists")
    new_group = await service.add_group(user_id=get_user_id_from_token(dependencies), group=group, db=db)
    content = str(new_group.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@groups.get("/names/{group_id}", response_model=List[str])
async def get_other_names_supply(group_id: int, db: Session = Depends(get_db)):
    names = await service.get_group_others_names(group_id, db)
    return names

@groups.put("", status_code=HTTP_200_OK)
async def update_group(data_update: GroupSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_group = await service.get_group_simple(data_update.id, db)
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_group = await service.update_group(user_id=get_user_id_from_token(dependencies), group=db_group, data_update=data_update, db=db)
    return Response(status_code=HTTP_200_OK)

@groups.delete("/{group_id}", response_model=List[str])
async def delete_group(group_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_group = await service.get_group_simple(group_id, db)
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_group(user_id=get_user_id_from_token(dependencies), group=db_group, db=db)
    return Response(status_code=HTTP_204_NO_CONTENT)

# Upload image to groups folder
@groups.post("/{group_id}", status_code=HTTP_201_CREATED)
async def add_image(group_id: int, file: UploadFile, dependencies=Depends(JWTBearer())):
    await service.add_image(user_id=get_user_id_from_token(dependencies), group_id=group_id, file=file)
    return Response(status_code=HTTP_201_CREATED)

# Get images from groups folder
@groups.get("/image/{group_id}")
async def get_images(group_id: int):
    images = await service.get_images(group_id)
    return images

# Delete images to groups folder
@groups.delete("/image/{group_id}", status_code=HTTP_200_OK)
async def delete_image(group_id: int, file: UploadFile, dependencies=Depends(JWTBearer())):
    await service.delete_image(user_id=get_user_id_from_token(dependencies), group_id=group_id, file=file)
    return Response(status_code=HTTP_200_OK)