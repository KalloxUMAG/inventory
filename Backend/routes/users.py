import re
import os

from typing import List, Union, Any
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy import false
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from jose import jwt

from passlib.context import CryptContext

from fastapi import Depends, APIRouter, HTTPException, status, Response, UploadFile
from fastapi.security import OAuth2PasswordBearer
from schemas.user_schema import (
    FilterUser,
    TokenSchema,
    requestdetails,
    changepassword,
    UserCreate,
    UserEdit,
)
from schemas.role_schema import GrantRoleSchema

from config.settings import settings

from config.database import get_db
from sqlalchemy.orm import Session

from models.models import Users, TokenTable, UserGroupRoleRelation

from auth.auth_bearer import JWTBearer
from functools import wraps
from routes.groups import get_group

from auth.auth_bearer import JWTBearer
from functools import wraps

users = APIRouter(
    tags=["users"], prefix="/api/users", dependencies=[Depends(JWTBearer())]
)
login = APIRouter(tags=["users"], prefix="/api/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 5  # 5 dia
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs["dependencies"], SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        data = (
            kwargs["session"]
            .query(TokenTable)
            .filter_by(user_id=user_id, access_toke=kwargs["dependencies"], status=True)
            .first()
        )
        if data:
            return func(kwargs["dependencies"], kwargs["session"])

        else:
            return {"msg": "Token blocked"}

    return wrapper


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> bool:
    return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta

    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "iat": datetime.utcnow()}
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


@users.post("", status_code=HTTP_201_CREATED, tags=["users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    username = user.username.lower()
    email = user.email.lower()
    if db.query(Users).filter(Users.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(Users).filter(Users.email == email).first():
        raise HTTPException(status_code=400, detail="Email already taken")
    hashed_password = get_hashed_password(user.password)
    new_user = Users(
        username=user.username,
        fullname=user.fullname,
        hashed_password=hashed_password,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    content = str(new_user.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@users.put("", status_code=HTTP_200_OK)
def update_group(data_update: UserEdit, db: Session = Depends(get_db)):
    db_user = (
        db.query(Users)
        .filter(
            Users.id == data_update.id,
        )
        .first()
    )
    if not db_user:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return Response(status_code=HTTP_200_OK)


@login.post("/login", response_model=TokenSchema, tags=["users"])
def loginuser(
    request: requestdetails,
    dependencies=[Depends(JWTBearer())],
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.email == request.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
        )
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(
        user_id=user.id, access_toke=access, refresh_toke=refresh, status=True
    )
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {"access_token": access, "refresh_token": refresh, "fullname": user.fullname}


@users.get("", tags=["users"])
def getusers(session: Session = Depends(get_db)):
    user = session.query(Users).all()
    return user

@users.get("/{user_id}", tags=["users"], response_model=FilterUser)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(Users).filter(Users.id == user_id).first()
    return user

@users.post("/change-password", tags=["users"])
def change_password(
    request: changepassword,
    dependencies=Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    token = dependencies
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]
    if not request.email:
        user = db.query(Users).filter(Users.id == user_id).first()
    else:
        user = db.query(Users).filter(Users.email == request.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password"
        )

    encrypted_password = get_hashed_password(request.new_password)
    user.hashed_password = encrypted_password
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}


@users.post("/logout", tags=["users"])
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    token = dependencies
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]
    token_record = db.query(TokenTable).all()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = (
            db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        )
        db.commit()

    existing_token = (
        db.query(TokenTable)
        .filter(TokenTable.user_id == user_id, TokenTable.access_toke == token)
        .first()
    )
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}

@users.get("/search_users", tags=["users"], response_model=List[FilterUser])
def search_users(fullname: str = None, email: str = None, db: Session = Depends(get_db)):
    query = db.query(Users)

    if fullname is not None:
        query = query.filter(Users.fullname.ilike(f"%{fullname}%"))

    if email is not None:
        query = query.filter(Users.email.ilike(f"%{email}%"))

    query = query.filter(Users.disable.is_(False))

    users = query.all()

    result = []
    for user in users:
        filter_user = FilterUser(
            id=user.id,
            username=user.username,
            fullname=user.fullname,
            email=user.email,
            # ... (otros campos)
        )
        result.append(filter_user)

    return result

    return users

@users.post("/roles", status_code=HTTP_201_CREATED)
def grant_role_user(grant_role: GrantRoleSchema, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == grant_role.user_id).first()
    if not db_user:
        return Response(
            status_code=HTTP_404_NOT_FOUND, content={"message": "User not found in database"}
        )
    db_group = get_group(grant_role.group_id, db=db)
    if not db_group:
        return Response(
            status_code=HTTP_404_NOT_FOUND, content={"message": "Group not found in database"}
        )
    new_grant_role = UserGroupRoleRelation(
        user_id=grant_role.user_id, role_id=grant_role.role_id, group_id=grant_role.group_id
    )
    db.add(new_grant_role)
    db.commit()
    db.refresh(new_grant_role)
    content = str(new_grant_role)
    return Response(status_code=HTTP_201_CREATED, content=content)

# images

# Upload image to users folder
@users.post("/images/{user_id}", status_code=HTTP_201_CREATED)
async def add_image(user_id: int, file: UploadFile):
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
    return Response(status_code=HTTP_201_CREATED)

# Get images from users folder
@users.get("/images/{user_id}")
async def get_images(user_id: int):
    image_path = Path(settings.image_directory, "users", str(user_id))
    if not image_path.exists():
        print("No images found")
        return Response(status_code=HTTP_404_NOT_FOUND)

    image_base_url = settings.base_url.path.replace("/api", "/images")
    return [
        {
            "id": i,
            "name": file.name,
            "path": f"{image_base_url}/users/{user_id}/{file.name}",
        }
        for i, file in enumerate(image_path.iterdir(), start=1)
    ]

# Delete images to groups folder
@users.delete("/images/{user_id}", status_code=HTTP_200_OK)
async def delete_image(user_id: int, file: UploadFile):
    image_path = Path(settings.image_directory, "users", str(user_id))
    image_path.mkdir(parents=True, exist_ok=True)
    extension = file.filename.split(".")[-1].lower()
    format_filename = file.filename[: -len(extension)].lower()
    format_filename = re.sub("[^A-Za-z0-9_]", "", format_filename, 0, re.IGNORECASE)
    os.remove(str(image_path) + "/" + str(format_filename) + "." + str(extension))
    return Response(status_code=HTTP_200_OK)
