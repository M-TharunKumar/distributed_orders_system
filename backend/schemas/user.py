from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role: str


class UserResponse(UserBase):
    user_id: int
    role: str

    class Config:
        from_attributes = True