from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from auth.dependencies import require_viewer

from services.report_service import (
    get_inventory_report,
    get_customer_report,
    get_summary_report
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/inventory")
def inventory_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    return {
        "generated_by": current_user.username,
        "report": get_inventory_report(db)
    }


@router.get("/customers")
def customer_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    return {
        "generated_by": current_user.username,
        "report": get_customer_report(db)
    }


@router.get("/summary")
def summary_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    return {
        "generated_by": current_user.username,
        "report": get_summary_report(db)
    }