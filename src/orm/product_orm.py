from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.orm.base import Base

class ProductOrm(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    price = Column(Float, nullable=False)
    human_volume = Column(String, nullable=False)
    volume = Column(Float, nullable=False)
    volume_type = Column(String, nullable=False)
    price_type = Column(String, nullable=False)

    slug = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    image_urls = Column(String, nullable=False)
    canonical_url = Column(String, nullable=False)



    cart_item_id = Column(Integer, ForeignKey('cart_items.id'), nullable=False)

    item = relationship("CartItemOrm", back_populates="product")



