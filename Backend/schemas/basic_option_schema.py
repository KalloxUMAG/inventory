from pydantic import BaseModel


class BasicOptionSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True

# No inheritance from BasicOptionSchema because can't reorder fields
class BasicOptionSchemaWithId(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ModelSchema(BaseModel):
    name: str
    brand_id: int

    class Config:
        from_attributes = True

class ModelSchemaWithId(ModelSchema):
    id: int
    name: str
    brand_id: int

    class Config:
        from_attributes = True