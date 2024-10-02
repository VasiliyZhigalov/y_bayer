from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from src.models.product import Product
from src.models.shop import Shop


class CartItem(BaseModel):
    id: Optional[int] = None
    quantity: int
    request_product_name: str  # запрос,
    product: Product
    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    id: Optional[int] = None
    user_id: int
    shop: Shop
    total_price: float = 0.
    items: List[CartItem] = []

    model_config = ConfigDict(from_attributes=True)
