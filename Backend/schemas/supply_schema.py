from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplyListSchema(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    state: Optional[bool] = None
    stock: Optional[int] = None
    lot_stock: Optional[int] = None
    critical_stock: Optional[int] = None
    samples: Optional[float] = None
    observation: Optional[str] = None
    supplies_brand_name: Optional[str] = None
    supplies_type_name: Optional[str] = None
    supplies_format_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True


class SupplySchemaFull(BaseModel):
    id: Optional[int] = None
    name: str
    code: Optional[str] = None
    state: Optional[bool] = None
    stock: Optional[int] = None
    lot_stock: Optional[int] = None
    critical_stock: Optional[int] = None
    samples: Optional[float] = None
    observation: Optional[str] = None
    supplies_brand_id: Optional[int] = None
    supplies_type_id: Optional[int] = None
    supplies_format_id: Optional[int] = None
    supplies_brand_name: Optional[str] = None
    supplies_type_name: Optional[str] = None
    supplies_format_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True


class SupplySchema(BaseModel):
    id: Optional[int] = None
    name: str
    code: Optional[str] = None
    state: Optional[bool] = None
    stock: Optional[int] = None
    lot_stock: Optional[int] = None
    critical_stock: Optional[int] = None
    samples: Optional[float] = None
    observation: Optional[str] = None
    supplies_brand_id: Optional[int] = None
    supplies_type_id: Optional[int] = None
    supplies_format_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True


class UpdateStockSchema(BaseModel):
    stock: int

    model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
