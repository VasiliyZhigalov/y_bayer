from typing import Optional

from pydantic import BaseModel, ConfigDict


class Shop(BaseModel):
    id: Optional[int] = None
    name: str
    url: str  # URL для парсинга
    model_config = ConfigDict(from_attributes=True)
