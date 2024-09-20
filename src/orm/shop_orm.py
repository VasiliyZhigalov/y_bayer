from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from src.orm.base import Base
from sqlalchemy.orm import relationship


class ShopOrm(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    carts = relationship("CartOrm", back_populates="shop")
