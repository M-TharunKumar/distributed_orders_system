from decimal import Decimal


def calculate_discount(
    amount: Decimal
) -> Decimal:

    if amount >= Decimal("50000"):
        return amount * Decimal("0.10")

    if amount >= Decimal("20000"):
        return amount * Decimal("0.05")

    return Decimal("0.00")


def calculate_final_amount(
    quantity: int,
    unit_price: Decimal
):
    total_amount = (
        Decimal(quantity) * unit_price
    )

    discount = calculate_discount(
        total_amount
    )

    final_amount = (
        total_amount - discount
    )

    return {
        "total_amount": total_amount,
        "discount": discount,
        "final_amount": final_amount
    }