import re

from typing import List
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, Response, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from config.settings import settings
from models.models import Groups, GroupOtherNames
from schemas.group_schema import CreateGroupSchema, GroupSchema

from auth.auth_bearer import JWTBearer

groups = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["groups"], prefix="/api/groups"
)


@groups.get("", response_model=List[GroupSchema])
def get_groups(db: Session = Depends(get_db)):
    results_db = db.query(Groups.id, Groups.name, Groups.description).all()
    results = [
        GroupSchema(
            id = result.id,
            name = result.name,
            description = result.description,
            other_names = get_other_names_supply(result.id, db),
            ) for result in results_db]
    return results

@groups.get("/{group_id}", response_model=GroupSchema)
def get_group(group_id: int, db: Session = Depends(get_db)):
    result_db = db.query(Groups).filter(Groups.id == group_id).first()
    result = GroupSchema(
        id = result_db.id,
        name = result_db.name,
        description = result_db.description,
        other_names = get_other_names_supply(result_db.id, db),
        )
    return result
  
@groups.post("", status_code=HTTP_201_CREATED)
def add_groups(group: CreateGroupSchema, db: Session = Depends(get_db)):
    db_group = (
        db.query(Groups).filter(func.lower(Groups.name) == group.name.lower()).first()
    )
    if db_group:
        return Response(status_code=HTTP_409_CONFLICT, content="Group already exists")
    new_group = Groups(name=group.name, description=group.description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    new_group_id = new_group.id
    if group.other_names:
        for name in group.other_names:
            db.add(GroupOtherNames(group_id=new_group_id, name=name))
            db.commit()
    content = str(new_group.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@groups.get("/names/{group_id}", response_model=List[str])
def get_other_names_supply(group_id: int, db: Session = Depends(get_db)):
    results_db = db.query(GroupOtherNames).filter(GroupOtherNames.group_id == group_id).all()
    results = [result.name for result in results_db]
    return results

# Upload image to groups folder
@groups.post("/{group_id}", status_code=HTTP_201_CREATED)
async def add_image(group_id: int, file: UploadFile):
    image_path = Path(settings.image_directory, "groups", str(group_id))
    image_path.mkdir(parents=True, exist_ok=True)
    extension = file.filename.split(".")[-1].lower()
    format_filename = file.filename[: -len(extension)].lower()
    format_filename = re.sub("[^A-Za-z0-9]", "", format_filename, 0, re.IGNORECASE)
    date_now = datetime.now()
    date_now = date_now.strftime("%d%m%Y_%H%M%S")
    with open(
        str(image_path)
        + "/"
        + str(date_now)
        + str(format_filename)
        + "."
        + str(extension),
        "wb",
    ) as buffer:
        buffer.write(await file.read())
    return Response(status_code=HTTP_201_CREATED)

# Get images from groups folder
@groups.get("/image/{group_id}")
async def get_images(group_id: int):
    image_path = Path(settings.image_directory, "groups", str(group_id))
    if not image_path.exists():
        print("No images found")
        return Response(status_code=HTTP_404_NOT_FOUND)

    image_base_url = settings.base_url.path.replace("/api", "/images")
    return [
        {
            "id": i,
            "name": file.name,
            "path": f"{image_base_url}/groups/{group_id}/{file.name}",
        }
        for i, file in enumerate(image_path.iterdir(), start=1)
    ]