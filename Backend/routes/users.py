from typing import Annotated, Union, Any
from datetime import datetime, timedelta

from jose import jwt, JWTError

from passlib.context import CryptContext

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user_schema import UserInDB, TokenSchema, requestdetails, changepassword

from config.database import get_db
from sqlalchemy.orm import Session

from models.models import Users, TokenTable

from routes.auth_bearer import JWTBearer

users = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "32375e2ab7aded81e59257233f4c014b94ea0498206a0e2754e3b2221d58f272"
REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3


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

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

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


@users.post("/api/users", tags=["users"])
async def create_user(user: UserInDB, db: Session = Depends(get_db)):
    username = user.username.lower()
    email = user.email.lower()
    if db.query(Users).filter(Users.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(Users).filter(Users.email == email).first():
        raise HTTPException(status_code=400, detail="Email already taken")
    hashed_password = get_hashed_password(user.hashed_password)
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


@users.post("/login", response_model=TokenSchema, tags=["users"])
def login(request: requestdetails, db: Session = Depends(get_db)):
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
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@users.get("/getusers", tags=["users"])
def getusers(dependencies=Depends(JWTBearer()), session: Session = Depends(get_db)):
    user = session.query(Users).all()
    return user


@users.post("/change-password", tags=["users"])
def change_password(request: changepassword, db: Session = Depends(get_db)):
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
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}
