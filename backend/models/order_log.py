from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.orm import relationship

from database import Base


class OrderLog(Base):
    __tablename__ = "order_logs"

    log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    reason = Column(
        String(255),
        nullable=True
    )

    timestamp = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    order = relationship(
        "Order",
        back_populates="logs"
    )