from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column   
from datetime import date, datetime, UTC
from typing import List


# Create a base class for declarative models
class Base(DeclarativeBase):
    pass

# Instantiate the SQLAlchemy database
db = SQLAlchemy (model_class = Base)


# Junction Table for Many-to-Many relationship between service_tickets and mechanics
service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

# Junction Table for Many-to-Many relationship between service_tickets and inventories
service_inventory = db.Table(
    'service_inventory',
    Base.metadata,
    db.Column('service_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.ForeignKey('inventories.id'), primary_key=True)
)


# CLASSES
class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False) 

    # Relationship Attribute
    service_tickets: Mapped[List['Service_Ticket']] = db.relationship(back_populates='customer')

#class MechanicServiceTicket(Base):
    #__tablename__ = "MechanicServiceTicket"

    #id: Mapped[int] = mapped_column(primary_key=True)
    #mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), nullable=False)
    #service_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), nullable=False)
    #start_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    #mechanic: Mapped['Mechanic'] = db.relationship(back_populates='mechanic_tickets')
    #service_ticket: Mapped['Service_Ticket'] = db.relationship(back_populates='mechanic_tickets')


class Service_Ticket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    # Relationship Attribute
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanic, back_populates='service_tickets')
    inventories: Mapped[List['Inventory']] = db.relationship(secondary=service_inventory, back_populates= 'service_tickets')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Relationship Attribute
    service_tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=service_mechanic, back_populates='mechanics')

class Inventory(Base):
    __tablename__ = 'inventories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Relationship Attribute
    service_tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=service_inventory, back_populates='inventories')


