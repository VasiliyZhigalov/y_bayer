from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from src.orm.base import Base
from src.orm.shop_orm import ShopOrm


class CartOrm(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)

    user = relationship("UserOrm", back_populates="carts")
    items = relationship("CartItemOrm", back_populates="cart")
    shop = relationship("ShopOrm", back_populates="carts")


class CartItemOrm(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("CartOrm", back_populates="items")
    product = relationship("ProductOrm", back_populates="item", uselist=False)
