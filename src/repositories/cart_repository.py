from typing import List

from sqlalchemy.orm import Session
from src.orm.cart_orm import CartOrm
from src.models.cart import Cart
from src.repositories.base_repository import BaseRepository


class CartRepository(BaseRepository[CartOrm, Cart]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> Cart:
        orm_cart = self.session.query(CartOrm).filter(CartOrm.id == id).first()
        return Cart.model_validate(orm_cart, from_attributes=True)

    def get_all(self) -> List[Cart]:
        orm_carts = self.session.query(CartOrm).all()
        return [Cart.model_validate(cart, from_attributes=True) for cart in orm_carts]

    def create(self, entity: Cart) -> Cart:
        orm_cart = CartOrm(**entity.dict())
        self.session.add(orm_cart)
        self.session.commit()
        self.session.refresh(orm_cart)
        return Cart.model_validate(orm_cart, from_attributes=True)

    def update(self, id: int, entity: Cart) -> Cart:
        orm_cart = self.session.query(CartOrm).filter(CartOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_cart, key, value)
        self.session.commit()
        return Cart.model_validate(orm_cart, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_cart = self.session.query(CartOrm).filter(CartOrm.id == id).first()
        self.session.delete(orm_cart)
        self.session.commit()
