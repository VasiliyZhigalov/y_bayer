from pydantic import BaseModel, ConfigDict


class CartItem(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    id: int
    user_id: int
    shop_id: int
    total_price: float = 0.

    model_config = ConfigDict(from_attributes=True)  
