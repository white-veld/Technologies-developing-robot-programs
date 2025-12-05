from typing import Optional
from uuid import UUID, uuid4
from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Date, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUIDType


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
        nullable=False
    )


class Departments(Base):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    employees: Mapped[list["Employees"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Employees(Base):
    __tablename__ = "employees"
    full_name: Mapped[str] = mapped_column(String(70), nullable=False)
    position: Mapped[str] = mapped_column(String(40), nullable=False)
    department_id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False
    )
    department: Mapped["Departments"] = relationship(back_populates="employees")
    orders: Mapped[list["Orders"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Suppliers(Base):
    __tablename__ = "suppliers"
    company_name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(50), nullable=False)
    products: Mapped[list["Products"]] = relationship(
        back_populates="supplier"
    )


class Products(Base):
    __tablename__ = "products"
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    current_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    min_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    supplier_id: Mapped[Optional[UUID]] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        nullable=True
    )
    supplier: Mapped[Optional["Suppliers"]] = relationship(back_populates="products")
    order_items: Mapped[list["OrderItems"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Orders(Base):
    __tablename__ = "orders"
    employee_id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    employee: Mapped["Employees"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItems"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class OrderItems(Base):
    __tablename__ = "order_items"
    order_id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped["Orders"] = relationship(back_populates="items")
    product: Mapped["Products"] = relationship(back_populates="order_items")


def create_db(engine):
    Base.metadata.create_all(engine)


def drop_all_tables(engine):
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    engine = create_engine("sqlite:///company_data.db")
    create_db(engine)
