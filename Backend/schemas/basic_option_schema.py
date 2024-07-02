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

class UnitSchema(BaseModel):
    name: str
    building_id: int

    class Config:
        from_attributes = True

class UnitSchemaWithId(UnitSchema):
    id: int
    name: str
    building_id: int

    class Config:
        from_attributes = True

class RoomSchema(BaseModel):
    name: str
    unit_id: int

    class Config:
        from_attributes = True

class RoomSchemaWithId(RoomSchema):
    id: int
    name: str
    unit_id: int

    class Config:
        from_attributes = True

class ProjectSchema(BaseModel):
    name: str
    owner_id: int

    class Config:
        from_attributes = True

class ProjectSchemaWithId(ProjectSchema):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True

class StageSchema(BaseModel):
    name: str
    project_id: int

    class Config:
        from_attributes = True

class StageSchemaWithId(StageSchema):
    id: int
    name: str
    project_id: int

    class Config:
        from_attributes = True