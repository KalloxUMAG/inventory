from typing import List, Optional

from pydantic import BaseModel

from schemas.lot_schema import LotListSchema

# List of supplies and lots with their respective brands, types and formats
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
    supplies_brand_id: Optional[int] = None
    supplies_brand_name: Optional[str] = None
    supplies_type_id: Optional[int] = None
    supplies_type_name: Optional[str] = None
    supplies_format_id: Optional[int] = None
    supplies_format_name: Optional[str] = None
    lots: Optional[List[LotListSchema]] = None

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class UpdateStockSchema(BaseModel):
    stock: int

    class Config:
        from_attributes = True
