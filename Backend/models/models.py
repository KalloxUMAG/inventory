from typing import List, Optional

from sqlalchemy import Boolean, Date, Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from datetime import datetime
from config.database import Base

# Tablas independientes


class Building(Base):
    __tablename__ = "Buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    units: Mapped[List["Unit"]] = relationship(backref="Buildings", cascade="delete,merge")


class Invoice(Base):
    __tablename__ = "Invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer)
    date = mapped_column(Date)
    supplier_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Suppliers.id", ondelete="CASCADE")
    )

    equipments: Mapped[List["Equipment"]] = relationship(backref="Invoices")


class Brand(Base):
    __tablename__ = "Brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    models: Mapped[List["Model"]] = relationship(backref="Brands", cascade="all, delete")


class Model(Base):
    __tablename__ = "Models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Brands.id", ondelete="CASCADE")
    )

    model_numbers: Mapped[List["ModelNumber"]] = relationship(
        backref="Models", cascade="all, delete"
    )


class ModelNumber(Base):
    __tablename__ = "Model_numbers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String, nullable=False)
    model_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Models.id", ondelete="CASCADE")
    )

    equipments: Mapped[List["Equipment"]] = relationship(backref="Model_numbers")


class Project(Base):
    __tablename__ = "Projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Project_owners.id", ondelete="CASCADE")
    )

    stages: Mapped[List["Stage"]] = relationship(backref="Projects", cascade="delete,merge")
    lots: Mapped[List["Lot"]] = relationship(backref="Projects")


class ProjectOwner(Base):
    __tablename__ = "Project_owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    projects: Mapped[List["Project"]] = relationship(
        backref="Project_owners", cascade="delete,merge"
    )


class Supplier(Base):
    __tablename__ = "Suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    rut: Mapped[str] = mapped_column(String)
    city_address = mapped_column(String)

    supplier_contacts: Mapped[List["SupplierContact"]] = relationship(
        backref="Suppliers", cascade="delete,merge"
    )
    invoices: Mapped[List["Invoice"]] = relationship(backref="Suppliers", cascade="delete,merge")
    equipments: Mapped[List["Equipment"]] = relationship(backref="Suppliers")
    lots: Mapped[List["Lot"]] = relationship(backref="Suppliers", cascade="delete,merge")
    supplies: Mapped[List["Supply"]] = relationship(
        secondary="Suppliers_has_Supplies", back_populates="suppliers"
    )


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    fullname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    disable: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String)

    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="user")


class TokenTable(Base):
    __tablename__ = "Token"
    user_id: Mapped[int] = mapped_column(Integer)
    access_toke: Mapped[str] = mapped_column(String, primary_key=True)
    refresh_toke: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean)
    created_date = mapped_column(DateTime, default=datetime.now)


class Groups(Base):
    __tablename__ = "Groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    lots: Mapped[List["Lot"]] = relationship(backref="Groups")
    supplies: Mapped[List["Supply"]] = relationship(
        secondary="Groups_has_Supplies", back_populates="groups"
    )


# Tablas dependientes


class Equipment(Base):
    __tablename__ = "Equipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    serial_number: Mapped[Optional[str]] = mapped_column(String)
    umag_inventory_code: Mapped[Optional[str]] = mapped_column(String)
    reception_date = mapped_column(Date, nullable=True)
    maintenance_period: Mapped[Optional[int]] = mapped_column(Integer)
    observation: Mapped[Optional[str]] = mapped_column(String)
    next_maintenance: Mapped[Optional[Date]] = mapped_column(Date)

    supplier_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Suppliers.id", ondelete="SET NULL"), nullable=True
    )
    invoice_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Invoices.id", ondelete="SET NULL"), nullable=True
    )
    model_number_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Model_numbers.id", ondelete="SET NULL")
    )
    room_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("Rooms.id", ondelete="SET NULL")
    )
    stage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Stages.id", ondelete="SET NULL"), nullable=True
    )
    last_preventive_mainteinance = mapped_column(Date)

    maintenances: Mapped[List["Maintenance"]] = relationship(
        backref="Equipments", cascade="delete,merge"
    )

    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="equipment")


class Maintenance(Base):
    __tablename__ = "Maintenances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date = mapped_column(Date)
    observations: Mapped[str] = mapped_column(String)
    state: Mapped[bool] = mapped_column(Boolean, nullable=True)
    maintenance_type: Mapped[str] = mapped_column(String)
    equiptment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Equipments.id", ondelete="CASCADE")
    )


class Room(Base):
    __tablename__ = "Rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    unit_id: Mapped[int] = mapped_column(Integer, ForeignKey("Units.id", ondelete="CASCADE"))

    equipments: Mapped[List["Equipment"]] = relationship(backref="Rooms")


class Role(Base):
    __tablename__ = "Roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)


class Stage(Base):
    __tablename__ = "Stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"))


class SupplierContact(Base):
    __tablename__ = "Supplier_contact"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    supplier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Suppliers.id", ondelete="CASCADE")
    )


class Unit(Base):
    __tablename__ = "Units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    building_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Buildings.id", ondelete="CASCADE")
    )

    rooms: Mapped[List["Room"]] = relationship(backref="Units", cascade="delete,merge")


# Relaciones N - M


# ------------Insumos----------------------------


class Supply(Base):
    __tablename__ = "Supplies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    state: Mapped[bool] = mapped_column(Boolean)
    stock: Mapped[int] = mapped_column(Integer)
    lot_stock: Mapped[int] = mapped_column(Integer)
    critical_stock: Mapped[int] = mapped_column(Integer)
    samples: Mapped[float] = mapped_column(Float)
    observation: Mapped[str] = mapped_column(String)

    supplies_brand_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Supplies_brands.id", ondelete="CASCADE")
    )
    supplies_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Supplies_types.id", ondelete="CASCADE")
    )
    supplies_format_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Supplies_formats.id", ondelete="CASCADE")
    )

    lots: Mapped[List["Lot"]] = relationship(backref="Supplies", cascade="delete,merge")
    suppliers: Mapped[List["Supplier"]] = relationship(
        secondary="Suppliers_has_Supplies", back_populates="supplies"
    )
    groups: Mapped[List["Groups"]] = relationship(
        secondary="Groups_has_Supplies", back_populates="supplies"
    )


class SupplyBrand(Base):
    __tablename__ = "Supplies_brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    supplies: Mapped[List["Supply"]] = relationship(
        backref="Supplies_brands", cascade="delete,merge"
    )


class SupplyType(Base):
    __tablename__ = "Supplies_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    supplies: Mapped[List["Supply"]] = relationship(
        backref="Supplies_types", cascade="delete,merge"
    )


class SupplyFormat(Base):
    __tablename__ = "Supplies_formats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    supplies: Mapped[List["Supply"]] = relationship(
        backref="Supplies_formats", cascade="delete,merge"
    )


class Location(Base):
    __tablename__ = "Locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    sub_locations: Mapped[List["SubLocation"]] = relationship(
        backref="Locations", cascade="delete,merge"
    )


class SubLocation(Base):
    __tablename__ = "Sub_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Locations.id", ondelete="CASCADE")
    )

    lots: Mapped[List["Lot"]] = relationship(backref="Sub_locations")


class Lot(Base):
    __tablename__ = "Lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String)  # Numero unico por cada lote (puede tener letras)
    reception_date = mapped_column(Date)
    due_date = mapped_column(Date)
    observations: Mapped[str] = mapped_column(String)
    state: Mapped[bool] = mapped_column(Boolean)

    supplies_id: Mapped[int] = mapped_column(Integer, ForeignKey("Supplies.id", ondelete="CASCADE"))
    supplier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Suppliers.id", ondelete="CASCADE")
    )
    sub_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("Sub_locations.id"))
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("Projects.id"))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("Groups.id"))


class GroupsHasSupplies(Base):
    __tablename__ = "Groups_has_Supplies"

    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Groups.id", ondelete="CASCADE"), primary_key=True
    )
    supply_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Supplies.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer)


class SuppliersHasSupplies(Base):
    __tablename__ = "Suppliers_has_Supplies"

    supplier_id = mapped_column(
        Integer, ForeignKey("Suppliers.id", ondelete="CASCADE"), primary_key=True
    )
    supply_id = mapped_column(
        Integer, ForeignKey("Supplies.id", ondelete="CASCADE"), primary_key=True
    )
    cost: Mapped[int] = mapped_column(Integer)

class Loan(Base):
    __tablename__ = "Loans"

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("Users.id"))
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("Equipments.id"))
    loan_start_date = mapped_column(Date, nullable=False)
    loan_end_date = mapped_column(Date, nullable=False)

    user: Mapped[Users] = relationship("Users", back_populates="loans")
    equipment: Mapped[Equipment] = relationship("Equipment", back_populates="loans")
class UserGroupRoleRelation(Base):
    __tablename__ = "User_Group_Role_Relation"

    user_id = mapped_column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    group_id = mapped_column(Integer, ForeignKey("Groups.id", ondelete="CASCADE"), primary_key=True)
    role_id = mapped_column(Integer, ForeignKey("Roles.id", ondelete="CASCADE"), primary_key=True)
