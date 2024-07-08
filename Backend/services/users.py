import re
import os
from datetime import datetime, timedelta
from fastapi import UploadFile
from pathlib import Path
from config.settings import settings
from sqlalchemy import false
from sqlalchemy.orm import Session
from models.models import Users
from schemas.user_schema import UserCreate, UserEdit, FilterUser

class UserService:
    async def get_user_by_username(self, username: str, db: Session):
        return db.query(Users).filter(Users.username == username).first()
    async def get_user_by_email(self, email: str, db: Session):
        return db.query(Users).filter(Users.email == email).first()
    async def get_users(self, db: Session):
        return db.query(Users).all()
    async def create_user(self, user: UserCreate, hashed_password: str, db: Session):
        new_user = Users(
            username=user.username,
            fullname=user.fullname,
            hashed_password=hashed_password,
            email=user.email,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    async def get_user(self, user_id: int, db: Session):
        return db.query(Users).filter(Users.id == user_id).first()
    async def search_users(self, db: Session, fullname: str = None, email: str = None):
        query = db.query(Users)
        if fullname is not None:
            query = query.filter(Users.fullname.ilike(f"%{fullname}%"))
        if email is not None:
            query = query.filter(Users.email.ilike(f"%{email}%"))
        query = query.filter(Users.disable.is_(False))
        users_db = query.all()
        users = []
        for user in users_db:
            filter_user = FilterUser(
                id=int(user.id),
                username=user.username,
                fullname=user.fullname,
                email=user.email,
                # ... (otros campos)
            )
            users.append(filter_user)
        return users
    async def update_user(self, user, data_update: UserEdit, db: Session):
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    async def get_user_images(self, user_id: int):
        image_path = Path(settings.image_directory, "users", str(user_id))
        if not image_path.exists():
            return []
        image_base_url = settings.base_url.path.replace("/api", "/images")
        return [
            {
                "id": i,
                "name": file.name,
                "path": f"{image_base_url}/users/{user_id}/{file.name}",
            }
            for i, file in enumerate(image_path.iterdir(), start=1)
        ]
    async def add_user_image(self, user_id: int, file: UploadFile):
        image_path = Path(settings.image_directory, "users", str(user_id))
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
    async def delete_user_images(self, user_id: int, file: UploadFile):
        image_path = Path(settings.image_directory, "users", str(user_id))
        image_path.mkdir(parents=True, exist_ok=True)
        extension = file.filename.split(".")[-1].lower()
        format_filename = file.filename[: -len(extension)].lower()
        format_filename = re.sub("[^A-Za-z0-9_]", "", format_filename, 0, re.IGNORECASE)
        os.remove(str(image_path) + "/" + str(format_filename) + "." + str(extension))