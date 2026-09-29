from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    order_id: int
    customer_id: int
    product_id: int

    quantity: int = Field(gt=0)

    unit_price: Decimal = Field(
        gt=0,
        decimal_places=2
    )

    payment_status: str = "PENDING"

    processing_status: str = "PENDING"

    retry_count: int = Field(
        default=0,
        ge=0
    )

    source: str

class OrderCreate(BaseModel):
    order_id: int
    customer_id: int
    product_id: int

    quantity: int = Field(gt=0)

    unit_price: Decimal = Field(
        gt=0,
        decimal_places=2
    )

    order_time: datetime | None = None

    payment_status: str = "PENDING"

    source: str


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    order_time: datetime
    payment_status: str
    processing_status: str
    retry_count: int
    source: str

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True