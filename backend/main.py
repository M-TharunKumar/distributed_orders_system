from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import Base, engine, get_db

import models

from routers.auth_router import router as auth_router
from routers.order_router import router as order_router
from routers.report_router import router as report_router


app = FastAPI(
    title="Distributed Order Processing & Recovery System",
    description=(
        "Order processing system with JWT authentication, "
        "inventory management, retry and recovery."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(report_router)


""" @app.get("/")
def root():
    return {
        "message": "Distributed Order Processing System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def database_test(
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("SELECT 1")
    )

    return {
        "database": "connected",
        "result": result.scalar()
    } """