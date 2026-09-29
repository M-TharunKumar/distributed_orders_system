from pydantic import BaseModel


class InventoryReport(BaseModel):
    product_id: int
    product_name: str
    available_stock: int
    reserved_stock: int


class CustomerReport(BaseModel):
    customer_id: int
    customer_name: str
    email: str
    total_orders: int
    total_amount: float


class SummaryReport(BaseModel):
    total_orders: int
    successful_orders: int
    rejected_orders: int
    failed_orders: int
    retried_orders: int
    duplicate_orders: int
    total_revenue: float