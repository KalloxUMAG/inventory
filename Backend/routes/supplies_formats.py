from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from config.database import get_db
from models.models import SupplyFormat
from schemas.supplies_format_schema import SuppliesFormatsSchema

from auth.auth_bearer import JWTBearer

supplies_formats = APIRouter(
    dependencies=[Depends(JWTBearer())],
    tags=["supplies"],
    prefix="/api/supplies_formats",
)


@supplies_formats.get("", response_model=List[SuppliesFormatsSchema])
def get_supplies_formats(db: Session = Depends(get_db)):
    result = db.query(SupplyFormat.id, SupplyFormat.name).all()
    return result


@supplies_formats.post("", status_code=HTTP_201_CREATED)
def add_supplies_format(sformat: SuppliesFormatsSchema, db: Session = Depends(get_db)):
    db_supplies_format = (
        db.query(SupplyFormat)
        .filter(func.lower(SupplyFormat.name) == sformat.name.lower())
        .first()
    )
    if db_supplies_format:
        content = str(new_supplies_format.id)
        return Response(status_code=HTTP_200_OK, content=content)
    new_supplies_format = SupplyFormat(name=sformat.name)
    db.add(new_supplies_format)
    db.commit()
    db.refresh(new_supplies_format)
    content = str(new_supplies_format.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
