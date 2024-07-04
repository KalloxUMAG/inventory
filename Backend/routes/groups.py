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

from auth.auth_bearer import JWTBearer

groups = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["groups"], prefix="/api/groups"
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
async def add_groups(group: CreateGroupSchema, db: Session = Depends(get_db)):
    db_group = await service.get_group_by_name(group.name, db)
    if db_group:
        return Response(status_code=HTTP_409_CONFLICT, content="Group already exists")
    new_group = await service.add_group(group, db)
    content = str(new_group.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@groups.get("/names/{group_id}", response_model=List[str])
async def get_other_names_supply(group_id: int, db: Session = Depends(get_db)):
    names = await service.get_group_others_names(group_id, db)
    return names

@groups.put("", status_code=HTTP_200_OK)
async def update_group(data_update: GroupSchema, db: Session = Depends(get_db)):
    db_group = await service.get_group_simple(data_update.id, db)
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    update_group = await service.update_group(db_group, data_update, db)
    return Response(status_code=HTTP_200_OK)

@groups.delete("/{group_id}", response_model=List[str])
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = await service.get_group_simple(group_id, db)
    if not db_group:
        return Response(status_code=HTTP_404_NOT_FOUND)
    
    return Response(status_code=HTTP_204_NO_CONTENT)

# Upload image to groups folder
@groups.post("/{group_id}", status_code=HTTP_201_CREATED)
async def add_image(group_id: int, file: UploadFile):
    await service.add_image(group_id, file)
    return Response(status_code=HTTP_201_CREATED)

# Get images from groups folder
@groups.get("/image/{group_id}")
async def get_images(group_id: int):
    images = await service.get_images(group_id)
    return images

# Delete images to groups folder
@groups.delete("/image/{group_id}", status_code=HTTP_200_OK)
async def delete_image(group_id: int, file: UploadFile):
    await service.delete_image(group_id, file)
    return Response(status_code=HTTP_200_OK)