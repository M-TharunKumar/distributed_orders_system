from fastapi import HTTPException


VALID_PAYMENT_STATUSES = {
    "PAID",
    "PENDING",
    "FAILED"
}


def validate_payment_status(
    payment_status: str
):

    payment_status = payment_status.upper()

    if payment_status not in VALID_PAYMENT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment status"
        )

    return payment_status


def process_payment(
    payment_status: str
):
    payment_status = validate_payment_status(
        payment_status
    )

    if payment_status == "FAILED":
        raise HTTPException(
            status_code=402,
            detail="Payment failed"
        )

    if payment_status == "PENDING":
        raise HTTPException(
            status_code=409,
            detail="Payment is still pending"
        )

    return True