from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order import Order
from models.order_log import OrderLog


def check_duplicate_order(
    db: Session,
    order_id: int
):
    existing_order = (
        db.query(Order)
        .filter(
            Order.order_id == order_id
        )
        .first()
    )

    if existing_order:

        duplicate_log = OrderLog(
            order_id=existing_order.order_id,
            status="DUPLICATE",
            reason=(
                f"Duplicate order request "
                f"for order ID {order_id}"
            )
        )

        db.add(duplicate_log)
        db.commit()

        raise HTTPException(
            status_code=409,
            detail=f"Duplicate order ID: {order_id}"
        )

    return False