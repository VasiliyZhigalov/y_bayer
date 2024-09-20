from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class RequestItem(BaseModel):
    id: Optional[int] = None
    product_name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class UserRequest(BaseModel):
    id: Optional[int] = None
    user_id: int
    items: Optional[List[RequestItem]] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
