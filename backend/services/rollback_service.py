from sqlalchemy.orm import Session

from models.order_log import OrderLog
from models.product import Product

from services.inventory_service import release_stock


def rollback_order(
    db: Session,
    product: Product,
    quantity: int,
    order_id: int,
    reason: str
):
    release_stock(
        product,
        quantity
    )

    log = OrderLog(
        order_id=order_id,
        status="FAILED",
        reason=reason
    )

    db.add(log)

    db.commit()