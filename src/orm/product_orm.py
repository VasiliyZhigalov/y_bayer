from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.orm.base import Base

class ProductOrm(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    request_product_name = Column(String, nullable=False)
    cart_item_id = Column(Integer, ForeignKey('cart_items.id'), nullable=False)

    item = relationship("CartItemOrm", back_populates="product")



