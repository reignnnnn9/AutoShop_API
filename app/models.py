from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, String, Table, Column, Float, Integer
from datetime import date

# Create a base class for models
class Base(DeclarativeBase):
    pass

# Instantiate your SQLAlchemy database
db = SQLAlchemy(model_class=Base)


class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    DOB: Mapped[date] = mapped_column(Date, nullable=False)

    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', back_populates='customer', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Customer Name: {self.name}, Customer Email: {self.email}'

ticket_mechanics = db.Table(
    'ticket_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'), primary_key=True)
)

class ServiceTickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    ser_desc: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    ser_date: Mapped[date] = mapped_column(Date, nullable=False)

    customer: Mapped[list['Customers']] = relationship('Customers', back_populates='service_tickets')
    mechanics: Mapped[list['Mechanics']] = relationship('Mechanics', secondary=ticket_mechanics, back_populates='service_tickets')
    tick_inv: Mapped[list['TicketInventory']] = relationship('TicketInventory', back_populates='service_tickets')

class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    salary: Mapped[float] = mapped_column(Float(), nullable=False)

    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', secondary=ticket_mechanics, back_populates='mechanics')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    part: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    tick_inv: Mapped[list['TicketInventory']] = relationship('TicketInventory', back_populates='inventory')

class TicketInventory(Base):
    __tablename__ = "ticket_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    inv_id: Mapped[int] = mapped_column(ForeignKey('inventory.id'), nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('service_tickets.id'), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='tick_inv')
    service_tickets: Mapped['ServiceTickets'] = relationship('ServiceTickets', back_populates='tick_inv')