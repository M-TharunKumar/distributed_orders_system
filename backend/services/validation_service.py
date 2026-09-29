from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer
from models.product import Product


def validate_customer(
    db: Session,
    customer_id: int
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer_id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


def validate_product(
    db: Session,
    product_id: int
):
    product = (
        db.query(Product)
        .filter(
            Product.product_id == product_id
        )
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def validate_quantity(
    quantity: int
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )


def validate_price(
    unit_price: Decimal
):
    if unit_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Unit price must be greater than zero"
        )