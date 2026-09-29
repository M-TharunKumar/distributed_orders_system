from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order import Order
from models.order_log import OrderLog

from services.inventory_service import (
    reserve_stock,
    release_stock,
    confirm_reserved_stock
)

from services.payment_service import process_payment
from services.discount_service import calculate_final_amount


MAX_RETRIES = 3


def retry_order(
    db: Session,
    order_id: int
):

    # ========================================
    # FIND ORDER
    # ========================================

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


    # ========================================
    # CHECK SUCCESS
    # ========================================

    if order.processing_status == "SUCCESS":

        raise HTTPException(
            status_code=400,
            detail="Successful order cannot be retried"
        )


    # ========================================
    # CHECK MAX RETRIES
    # ========================================

    if order.retry_count >= MAX_RETRIES:

        raise HTTPException(
            status_code=400,
            detail="Maximum retry limit reached"
        )


    # ========================================
    # INCREMENT RETRY
    # ========================================

    order.retry_count += 1
    order.processing_status = "RETRIED"

    retry_log = OrderLog(
        order_id=order.order_id,
        status="RETRIED",
        reason=(
            f"Order retry attempt "
            f"{order.retry_count}"
        )
    )

    db.add(retry_log)

    db.commit()


    # ========================================
    # GET PRODUCT
    # ========================================

    product = order.product


    try:

        # ========================================
        # RESERVE STOCK
        # ========================================

        reserve_stock(
            product,
            order.quantity
        )


        reserved_log = OrderLog(
            order_id=order.order_id,
            status="RESERVED",
            reason=(
                f"Reserved {order.quantity} units "
                f"for retry attempt "
                f"{order.retry_count}"
            )
        )

        db.add(reserved_log)

        db.commit()


        # ========================================
        # PROCESS PAYMENT
        # ========================================

        process_payment(
            order.payment_status
        )


        # ========================================
        # CALCULATE AMOUNT
        # ========================================

        amount_details = calculate_final_amount(
            order.quantity,
            order.unit_price
        )


        # ========================================
        # CONFIRM RESERVATION
        # ========================================

        confirm_reserved_stock(
            product,
            order.quantity
        )


        # ========================================
        # SUCCESS
        # ========================================

        order.processing_status = "SUCCESS"


        success_log = OrderLog(
            order_id=order.order_id,
            status="SUCCESS",
            reason=(
                "Order successfully processed "
                "after retry"
            )
        )

        db.add(success_log)

        db.commit()

        db.refresh(order)

        return {
            "order": order,
            "amount_details": amount_details
        }


    except HTTPException as e:

        # ========================================
        # RELEASE STOCK
        # ========================================

        release_stock(
            product,
            order.quantity
        )


        released_log = OrderLog(
            order_id=order.order_id,
            status="RELEASED",
            reason=(
                f"Released {order.quantity} units "
                f"after retry failure"
            )
        )

        db.add(released_log)


        # ========================================
        # FAILED
        # ========================================

        order.processing_status = "FAILED"


        failed_log = OrderLog(
            order_id=order.order_id,
            status="FAILED",
            reason=str(e.detail)
        )

        db.add(failed_log)

        db.commit()

        raise e