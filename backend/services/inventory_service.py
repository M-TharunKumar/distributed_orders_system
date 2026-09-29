from fastapi import HTTPException


def check_stock(product, quantity):

    if product.available_stock < quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Insufficient stock for product "
                f"{product.product_id}. "
                f"Available: {product.available_stock}, "
                f"Requested: {quantity}"
            )
        )

    return True


def reserve_stock(product, quantity):

    check_stock(product, quantity)

    product.available_stock -= quantity
    product.reserved_stock += quantity


def release_stock(product, quantity):

    product.available_stock += quantity

    product.reserved_stock = max(
        0,
        product.reserved_stock - quantity
    )


def confirm_reserved_stock(product, quantity):

    product.reserved_stock = max(
        0,
        product.reserved_stock - quantity
    )