from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import fastapi_metadata as fm
from config.database import Base, engine
from config.settings import settings
from routes.brands import brands
from routes.buildings import buildings
from routes.equipments import equipments
from routes.invoices import invoices
from routes.locations import locations
from routes.lots import lots
from routes.maintenances import maintenances
from routes.model_numbers import model_numbers
from routes.models import models
from routes.project_owners import project_owners
from routes.projects import projects
from routes.rooms import rooms
from routes.stages import stages
from routes.sub_locations import sub_locations
from routes.supplier_contact import suppliers_contacts
from routes.suppliers import suppliers
from routes.Suppliers_supplies import suppliers_supplies
from routes.supplies import supplies
from routes.supplies_brands import supplies_brands
from routes.supplies_formats import supplies_formats
from routes.supplies_types import supplies_types
from routes.units import units
from routes.users import users
from routes.groups import groups
from routes.groups_supplies import groups_supplies


def create_tables():
    if not settings.production:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)


create_tables()

app = FastAPI(
    title=fm.title,
    description=fm.description,
    summary=fm.summary,
    version=fm.version,
    openapi_tags=fm.tags_metadata,
)
app.mount("/images", StaticFiles(directory=settings.image_directory), name="images")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)

routes = [
    buildings,
    brands,
    equipments,
    groups,
    groups_supplies,
    invoices,
    locations,
    lots,
    maintenances,
    models,
    model_numbers,
    units,
    projects,
    project_owners,
    rooms,
    stages,
    sub_locations,
    supplies,
    supplies_brands,
    supplies_formats,
    supplies_types,
    suppliers,
    suppliers_contacts,
    suppliers_supplies,
    users,
]

for route in routes:
    app.include_router(route)
