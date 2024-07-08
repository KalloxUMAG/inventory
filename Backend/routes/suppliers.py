from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from config.database import get_db
from services.suppliers import SupplierService
from schemas.supplier_schema import SupplierSchema, SupplierFullSchema, SupplierSchemaWithId, SupplierFullSchemaWithId

from auth.auth_bearer import JWTBearer, get_user_id_from_token

suppliers = APIRouter(
    dependencies=[Depends(JWTBearer())], tags=["suppliers"], prefix="/api/suppliers"
)
service = SupplierService()


@suppliers.get("", response_model=List[SupplierSchemaWithId])
async def get_suppliers(db: Session = Depends(get_db)):
    suppliers = await service.get_suppliers(db)
    return suppliers

@suppliers.get("/full", response_model=List[SupplierFullSchemaWithId])
async def get_suppliers_full(db: Session = Depends(get_db)):
    suppliers = await service.get_suppliers_full(db)
    return suppliers

@suppliers.post("", status_code=HTTP_201_CREATED)
async def add_supplier(supplier: SupplierFullSchema, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    new_supplier = await service.add_supplier(user_id=get_user_id_from_token(dependencies), supplier=supplier, db=db)
    content = str(new_supplier.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@suppliers.get("/{supplier_id}", response_model=SupplierSchemaWithId)
async def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = await service.get_supplier(supplier_id, db)
    if not supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return supplier


@suppliers.put("/{supplier_id}", response_model=SupplierSchemaWithId)
async def update_supplier(
    data_update: SupplierSchema, supplier_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)
):
    db_supplier = await service.get_supplier(supplier_id, db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier = await service.update_supplier(user_id=get_user_id_from_token(dependencies), supplier=db_supplier, data_update=data_update, db=db)
    return new_supplier


@suppliers.delete("/{supplier_id}", status_code=HTTP_200_OK)
async def delete_supplier(supplier_id: int, dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    db_supplier = await service.get_supplier(supplier_id, db)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    await service.delete_supplier(user_id=get_user_id_from_token(dependencies), supplier=db_supplier, db=db)
    return Response(status_code=HTTP_200_OK)
