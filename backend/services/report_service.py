from sqlalchemy.orm import Session
from sqlalchemy import func

from models.product import Product
from models.customer import Customer
from models.order import Order
from models.order_log import OrderLog


def get_inventory_report(db: Session):

    products = (
        db.query(Product)
        .order_by(Product.product_id)
        .all()
    )

    report = []

    for product in products:
        report.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "available_stock": product.available_stock,
            "reserved_stock": product.reserved_stock
        })

    return report


def get_customer_report(db: Session):

    customers = (
        db.query(Customer)
        .order_by(Customer.customer_id)
        .all()
    )

    report = []

    for customer in customers:

        successful_orders = (
            db.query(Order)
            .filter(
                Order.customer_id == customer.customer_id,
                Order.processing_status == "SUCCESS"
            )
            .all()
        )

        total_orders = len(successful_orders)

        total_amount = sum(
            float(order.quantity * order.unit_price)
            for order in successful_orders
        )

        report.append({
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "email": customer.email,
            "total_orders": total_orders,
            "total_amount": total_amount
        })

    return report


def get_summary_report(db: Session):

    successful_orders = (
        db.query(func.count(Order.order_id))
        .filter(
            Order.processing_status == "SUCCESS"
        )
        .scalar()
    )

    failed_orders = (
        db.query(OrderLog)
        .filter(
            OrderLog.status == "FAILED"
        )
        .count()
    )

    retried_orders = (
        db.query(OrderLog)
        .filter(
            OrderLog.status == "RETRIED"
        )
        .count()
    )

    rejected_orders = (
        db.query(OrderLog)
        .filter(
            OrderLog.status == "REJECTED"
        )
        .count()
    )

    duplicate_orders = (
        db.query(OrderLog)
        .filter(
            OrderLog.status == "DUPLICATE"
        )
        .count()
    )

    successful_order_records = (
        db.query(Order)
        .filter(
            Order.processing_status == "SUCCESS"
        )
        .all()
    )

    total_revenue = sum(
        float(
            order.quantity * order.unit_price
        )
        for order in successful_order_records
    )

    total_orders = (
        db.query(Order)
        .count()
    )

    return {
        "total_orders": total_orders,
        "successful_orders": successful_orders or 0,
        "rejected_orders": rejected_orders or 0,
        "failed_orders": failed_orders,
        "retried_orders": retried_orders,
        "duplicate_orders": duplicate_orders,
        "total_revenue": total_revenue
    }