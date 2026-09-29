from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    order_time = Column(
        DateTime,
        nullable=False
    )

    payment_status = Column(
        String(30),
        nullable=False,
        default="PENDING"
    )

    processing_status = Column(
    String(30),
    nullable=False,
    default="PENDING"
    )

    retry_count = Column(
    Integer,
    nullable=False,
    default=0
    )

    source = Column(
        String(30),
        nullable=False
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    product = relationship(
        "Product",
        back_populates="orders"
    )

    logs = relationship(
        "OrderLog",
        back_populates="order"
    )