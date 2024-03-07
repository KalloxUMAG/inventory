from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from config.database import get_db
from models.models import SupplyType
from schemas.supplies_type_schema import SuppliesTypesSchema

from auth.auth_bearer import JWTBearer

supplies_types = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["supplies"], prefix="/api/supplies_types"
)


@supplies_types.get("", response_model=List[SuppliesTypesSchema])
def get_supplies_types(db: Session = Depends(get_db)):
    result = db.query(SupplyType.id, SupplyType.name).all()
    return result


@supplies_types.post("", status_code=HTTP_201_CREATED)
def add_supplies_type(type: SuppliesTypesSchema, db: Session = Depends(get_db)):
    db_supplies_type = (
        db.query(SupplyType)
        .filter(func.lower(SupplyType.name) == type.name.lower())
        .first()
    )
    if db_supplies_type:
        content = str(db_supplies_type.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_supplies_type = SupplyType(name=type.name)
    db.add(new_supplies_type)
    db.commit()
    db.refresh(new_supplies_type)
    content = str(new_supplies_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
