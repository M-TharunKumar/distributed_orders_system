from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String(150),
        nullable=False
    )

    available_stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    reserved_stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    orders = relationship(
        "Order",
        back_populates="product"
    )