from sqlalchemy import Column, Integer, String, ForeignKey
from src.orm.base import Base
from sqlalchemy.orm import relationship


class UserOrm(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)  # Опциональный email пользователя

    requests = relationship("UserRequestOrm", back_populates="user", lazy='joined')
    carts = relationship("CartOrm", back_populates="user", lazy='joined')

