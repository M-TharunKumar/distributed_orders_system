from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database import get_db

from models.order import Order
from models.user import User

from schemas.order import (
    OrderCreate,
    OrderResponse
)

from auth.dependencies import (
    require_operator,
    require_viewer
)

from services.order_service import process_order
from services.retry_service import retry_order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/process",
    status_code=status.HTTP_201_CREATED
)
def process_order_api(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_operator)
):
    result = process_order(
        db,
        order_data
    )

    return {
        "message": "Order processed successfully",
        "processed_by": current_user.username,
        "order": result["order"],
        "amount_details": result["amount_details"]
    }


@router.get(
    "/{order_id}"
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "unit_price": order.unit_price,
        "order_time": order.order_time,
        "payment_status": order.payment_status,
        "source": order.source,
        "viewed_by": current_user.username
    }


@router.post(
    "/retry/{order_id}"
)
def retry_order_api(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_operator)
):
    result = retry_order(
        db,
        order_id
    )

    return {
        "message": "Order retry processed",
        "processed_by": current_user.username,
        "order": result["order"],
        "amount_details": result["amount_details"]
    }

@router.get("/")
def get_all_orders(
    status: str | None = None,
    source: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    query = db.query(Order)

    if status:
        query = query.filter(
            Order.processing_status == status.upper()
        )

    if source:
        query = query.filter(
            Order.source == source.upper()
        )

    orders = (
        query
        .order_by(Order.order_id.desc())
        .all()
    )

    return {
        "count": len(orders),
        "orders": [
            {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "unit_price": order.unit_price,
                "order_time": order.order_time,
                "payment_status": order.payment_status,
                "processing_status": order.processing_status,
                "retry_count": order.retry_count,
                "source": order.source
            }
            for order in orders
        ]
    }