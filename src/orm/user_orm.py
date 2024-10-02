from sqlalchemy import Column, Integer, String, Sequence
from src.orm.base import Base
from sqlalchemy.orm import relationship


class UserOrm(Base):
    __tablename__ = 'users'

    id = Column(Integer,  Sequence("fakemodel_id_sequence"), primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)  # Опциональный email пользователя

    requests = relationship("UserRequestOrm", back_populates="user", lazy='joined')
    carts = relationship("CartOrm", back_populates="user", lazy='joined')

