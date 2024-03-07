from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from models.models import ModelNumber
from routes.models import get_model
from schemas.model_number_schema import ModelNumberSchema

from auth.auth_bearer import JWTBearer

model_numbers = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["equipments"],
    prefix="/api/model_numbers",
)


@model_numbers.get("", response_model=List[ModelNumberSchema])
def get_model_numbers(db: Session = Depends(get_db)):
    result = db.query(ModelNumber).all()
    return result


@model_numbers.post("", status_code=HTTP_201_CREATED)
def add_model_number(model_number: ModelNumberSchema, db: Session = Depends(get_db)):
    db_model = get_model(model_number.model_id, db=db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_model_number = (
        db.query(ModelNumber)
        .filter(
            func.lower(ModelNumber.number) == model_number.number.lower(),
            ModelNumber.model_id == model_number.model_id,
        )
        .first()
    )
    if db_model_number:
        content = str(db_model_number.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_model_number = ModelNumber(
        number=model_number.number, model_id=model_number.model_id
    )
    db.add(new_model_number)
    db.commit()
    db.refresh(new_model_number)
    content = str(new_model_number.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@model_numbers.get("/model_number/{model_number_id}", response_model=ModelNumberSchema)
def get_model_number(model_number_id: int, db: Session = Depends(get_db)):
    return db.query(ModelNumber).filter(ModelNumber.id == model_number_id).first()


@model_numbers.get("/{model_id}", response_model=List[ModelNumberSchema])
def get_model_numbers_model(model_id: int, db: Session = Depends(get_db)):
    return db.query(ModelNumber).filter(ModelNumber.model_id == model_id).all()


@model_numbers.put("/{model_number_id}", response_model=ModelNumberSchema)
def update_model_number(
    data_update: ModelNumberSchema, model_number_id: int, db: Session = Depends(get_db)
):
    db_model_number = get_model_number(model_number_id, db=db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.model_dump(exclude_unset=True).items():
        setattr(db_model_number, key, value)
    db.add(db_model_number)
    db.commit()
    db.refresh(db_model_number)
    return db_model_number


@model_numbers.delete("/{model_number_id}", status_code=HTTP_204_NO_CONTENT)
def delete_model_number(model_number_id: int, db: Session = Depends(get_db)):
    db_model_number = get_model_number(model_number_id, db=db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_model_number)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
