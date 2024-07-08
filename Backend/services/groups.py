import re
import os
import shutil
from datetime import datetime
from pathlib import Path
from config.settings import settings

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.models import Groups, GroupOtherNames
from schemas.group_schema import CreateGroupSchema, GroupSchema

from services.logs import log_func_calls, CREATE_LOG, UPDATE_LOG, DELETE_LOG

class GroupService:
    async def get_group_others_names(self, group_id: int, db: Session):
        results_db = db.query(GroupOtherNames).filter(GroupOtherNames.group_id == group_id).all()
        results = [result.name for result in results_db]
        return results
    async def get_groups(self, db: Session):
        results_db = db.query(Groups.id, Groups.name, Groups.description).all()
        results = [
            GroupSchema(
                id = result.id,
                name = result.name,
                description = result.description,
                other_names = await self.get_group_others_names(result.id, db),
                ) for result in results_db]
        return results
    async def get_group(self, group_id: int, db: Session):
        result_db = db.query(Groups).filter(Groups.id == group_id).first()
        if not result_db:
            return None
        result = GroupSchema(
            id = result_db.id,
            name = result_db.name,
            description = result_db.description,
            other_names = await self.get_group_others_names(result_db.id, db),
            )
        return result
    async def get_group_simple(self, group_id: int, db: Session):
        return db.query(Groups).filter(Groups.id == group_id).first()
    async def get_group_by_name(self, name: str, db: Session):
        return db.query(Groups).filter(func.lower(Groups.name) == name.lower()).first()
    @log_func_calls("groups", CREATE_LOG)
    async def add_group(self, user_id: int, group: CreateGroupSchema, db: Session):
        new_group = Groups(name=group.name, description=group.description)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        new_group_id = new_group.id
        if group.other_names:
            for name in group.other_names:
                db.add(GroupOtherNames(group_id=new_group_id, name=name))
                db.commit()
        return new_group
    @log_func_calls("groups", UPDATE_LOG)
    async def update_group(self, user_id: int, group: GroupSchema, data_update: GroupSchema, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            if key != "other_names":
                setattr(group, key, value)
        db.add(group)
        db.commit()
        db.refresh(group)
        if data_update.other_names:
            db.query(GroupOtherNames).filter(GroupOtherNames.group_id == group.id).delete()
            for name in data_update.other_names:
                db.add(GroupOtherNames(group_id=group.id, name=name))
                db.commit()
        return group
    @log_func_calls("groups", DELETE_LOG)
    async def delete_group(self, user_id: int, group: GroupSchema, db: Session):
        db_group_names = db.query(GroupOtherNames).filter(GroupOtherNames.group_id == group.id).all()
        for group_name in db_group_names:
            db.delete(group_name)
            db.commit()
        db.delete(group)
        db.commit()
        image_path = Path(settings.image_directory, "groups", str(group.id))
        shutil.rmtree(image_path, ignore_errors=True)
        return group
    @log_func_calls("groups image", CREATE_LOG)
    async def add_image(self, user_id: int, group_id: int, file):
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
    async def get_images(self, group_id: int):
        image_path = Path(settings.image_directory, "groups", str(group_id))
        if not image_path.exists():
            return []

        image_base_url = settings.base_url.path.replace("/api", "/images")
        return [
            {
                "id": i,
                "name": file.name,
                "path": f"{image_base_url}/groups/{group_id}/{file.name}",
            }
            for i, file in enumerate(image_path.iterdir(), start=1)
        ]
    @log_func_calls("groups image", DELETE_LOG)
    async def delete_image(self, user_id: int, group_id: int, file):
        image_path = Path(settings.image_directory, "groups", str(group_id))
        image_path.mkdir(parents=True, exist_ok=True)
        extension = file.filename.split(".")[-1].lower()
        format_filename = file.filename[: -len(extension)].lower()
        format_filename = re.sub("[^A-Za-z0-9_]", "", format_filename, 0, re.IGNORECASE)
        os.remove(str(image_path) + "/" + str(format_filename) + "." + str(extension))