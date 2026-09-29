from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.order import Order
from models.order_log import OrderLog

from services.validation_service import (
    validate_customer,
    validate_product,
    validate_quantity,
    validate_price
)

from services.inventory_service import (
    reserve_stock,
    release_stock,
    confirm_reserved_stock
)

from services.payment_service import process_payment
from services.discount_service import calculate_final_amount
from services.duplicate_service import check_duplicate_order


def process_order(
    db: Session,
    order_data
):

    # ========================================
    # 1. CHECK DUPLICATE ORDER
    # ========================================

    check_duplicate_order(
        db,
        order_data.order_id
    )


    # ========================================
    # 2. VALIDATE CUSTOMER
    # ========================================

    customer = validate_customer(
        db,
        order_data.customer_id
    )


    # ========================================
    # 3. VALIDATE PRODUCT
    # ========================================

    product = validate_product(
        db,
        order_data.product_id
    )


    # ========================================
    # 4. CREATE ORDER
    # ========================================

    order = Order(
        order_id=order_data.order_id,
        customer_id=order_data.customer_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        unit_price=order_data.unit_price,
        order_time=order_data.order_time,
        payment_status=order_data.payment_status,
        processing_status="PROCESSING",
        retry_count=0,
        source=order_data.source
    )

    db.add(order)

    db.flush()


    # ========================================
    # 5. VALIDATE QUANTITY AND PRICE
    # ========================================

    try:

        validate_quantity(
            order_data.quantity
        )

        validate_price(
            order_data.unit_price
        )

    except HTTPException as e:

        order.processing_status = "REJECTED"

        log = OrderLog(
            order_id=order.order_id,
            status="REJECTED",
            reason=e.detail
        )

        db.add(log)

        db.commit()

        raise e


    # ========================================
    # 6. RESERVE STOCK
    # ========================================

    try:

        reserve_stock(
            product,
            order.quantity
        )

        # Log reservation
        reserved_log = OrderLog(
            order_id=order.order_id,
            status="RESERVED",
            reason=(
                f"Reserved {order.quantity} units "
                f"of product {product.product_id}"
            )
        )

        db.add(reserved_log)

        db.commit()


        # ========================================
        # 7. PROCESS PAYMENT
        # ========================================

        process_payment(
            order.payment_status
        )


        # ========================================
        # 8. CALCULATE DISCOUNT
        # ========================================

        amount_details = calculate_final_amount(
            order.quantity,
            order.unit_price
        )


        # ========================================
        # 9. CONFIRM STOCK
        # ========================================

        confirm_reserved_stock(
            product,
            order.quantity
        )


        # ========================================
        # 10. SUCCESS
        # ========================================

        order.processing_status = "SUCCESS"


        success_log = OrderLog(
            order_id=order.order_id,
            status="SUCCESS",
            reason="Order processed successfully"
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
        # RELEASE RESERVED STOCK
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
                f"of product {product.product_id}"
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


    except Exception as e:

        # ========================================
        # RELEASE RESERVED STOCK
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
                f"after unexpected error"
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
            reason=str(e)
        )

        db.add(failed_log)

        db.commit()


        raise HTTPException(
            status_code=500,
            detail="Order processing failed"
        )