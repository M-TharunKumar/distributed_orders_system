from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    customer_name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True