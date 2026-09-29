from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    product_name: str
    available_stock: int = Field(ge=0)
    reserved_stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True