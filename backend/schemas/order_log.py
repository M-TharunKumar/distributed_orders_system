from datetime import datetime

from pydantic import BaseModel


class OrderLogResponse(BaseModel):
    log_id: int
    order_id: int
    status: str
    reason: str | None = None
    timestamp: datetime

    class Config:
        from_attributes = True