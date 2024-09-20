from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.orm.base import Base


class UserRequestOrm(Base):
    __tablename__ = 'user_requests'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    # Связь
    user = relationship("UserOrm", back_populates="requests")
    items = relationship("RequestItemOrm", back_populates="request",lazy='joined', cascade="all, delete")



class RequestItemOrm(Base):
    __tablename__ = 'request_items'

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey('user_requests.id'))
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    request = relationship("UserRequestOrm", back_populates="items")
