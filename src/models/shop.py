from pydantic import BaseModel, ConfigDict


class Shop(BaseModel):
    id: int
    name: str
    url: str  # URL для парсинга
    cart_id: int
    model_config = ConfigDict(from_attributes=True)
