from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.token import LoginRequest, Token
from auth.password import verify_password
from auth.jwt import create_access_token


router = APIRouter(
    prefix="",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=Token
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(
            User.username == login_data.username
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    password_valid = verify_password(
        login_data.password,
        user.hashed_password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        username=user.username,
        role=user.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }