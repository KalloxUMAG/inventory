from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.model_numbers import ModelNumberService
from services.models import ModelService
from schemas.basic_option_schema import ModelNumberSchema, ModelNumberSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

model_numbers = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["equipments"],
    prefix="/api/model_numbers",
)
service = ModelNumberService()
model_service = ModelService()


@model_numbers.get("", response_model=List[ModelNumberSchemaWithId])
async def get_model_numbers(db: Session = Depends(get_db)):
    print(db)
    model_numbers = await service.get_model_numbers(db)
    return model_numbers


@model_numbers.post("", status_code=HTTP_201_CREATED)
async def add_model_number(model_number: ModelNumberSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_model = await model_service.get_model(model_number.model_id, db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_model_number = await service.add_model_number(user_id=get_user_id_from_token(dependencies), model_number=model_number, db=db)
    content = str(new_model_number.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@model_numbers.get("/model_number/{model_number_id}", response_model=ModelNumberSchemaWithId)
async def get_model_number(model_number_id: int, db: Session = Depends(get_db)):
    model_number = await service.get_model_number(model_number_id, db)
    if not model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return model_number


@model_numbers.get("/{model_id}", response_model=List[ModelNumberSchemaWithId])
async def get_model_numbers_model(model_id: int, db: Session = Depends(get_db)):
    model_numbers = await service.get_model_number_by_model(model_id, db)
    if not model_numbers:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return model_numbers


@model_numbers.put("/{model_number_id}", response_model=ModelNumberSchemaWithId)
async def update_model_number(
    data_update: ModelNumberSchema, model_number_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_model_number = await service.get_model_number(model_number_id, db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    model_number = await service.update_model_number(user_id=get_user_id_from_token(dependencies), model_number=db_model_number, data_update=data_update, db=db)
    return model_number


@model_numbers.delete("/{model_number_id}", status_code=HTTP_200_OK)
async def delete_model_number(model_number_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_model_number = await service.get_model_number(model_number_id, db)
    if not db_model_number:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_model_number(user_id=get_user_id_from_token(dependencies), model_number=db_model_number, db=db)
    return Response(status_code=HTTP_200_OK)
