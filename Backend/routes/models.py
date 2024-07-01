from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.models import ModelService
from services.brands import BrandService
from schemas.basic_option_schema import ModelSchema, ModelSchemaWithId

from auth.auth_bearer import JWTBearer

models = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["equipments"], prefix="/api/models"
)
service = ModelService()
brand_service = BrandService()

@models.get("", response_model=List[ModelSchemaWithId])
async def get_models(db: Session = Depends(get_db)):
    models = await service.get_models(db)
    return models


@models.post("", status_code=HTTP_201_CREATED)
async def add_model(model: ModelSchema, db: Session = Depends(get_db)):
    db_brand = await brand_service.get_brand(model.brand_id, db=db)
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND, content="Brand not found")
    model = await service.add_model(model, db=db)
    content = str(model.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@models.get("/model/{model_id}", response_model=ModelSchemaWithId)
async def get_model(model_id: int, db: Session = Depends(get_db)):
    model = await service.get_model(model_id, db)
    if not model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return model


@models.get("/{brand_id}", response_model=List[ModelSchemaWithId])
async def get_models_brand(brand_id: int, db: Session = Depends(get_db)):
    models = await service.get_models_brand(brand_id, db)
    return models


@models.put("/{model_id}", response_model=ModelSchemaWithId)
async def update_model(
    data_update: ModelSchema, model_id: int, db: Session = Depends(get_db)
):
    db_model = await service.get_model(model_id, db)
    if not db_model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_brand = await brand_service.get_brand(data_update.brand_id, db=db)
    if not db_brand:
        return Response(status_code=HTTP_404_NOT_FOUND, content="Brand not found")
    model = await service.update_model(db_model, data_update, db)
    return model


@models.delete("/{model_id}", status_code=HTTP_200_OK)
async def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = await service.get_model(model_id, db)
    if not model:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_model(model, db)
    return Response(status_code=HTTP_200_OK)
