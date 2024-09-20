from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    id: int
    name: str
    price: float
    request_product_name: str
    model_config = ConfigDict(from_attributes=True)

