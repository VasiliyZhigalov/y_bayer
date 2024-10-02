from itertools import product
from logging import setLogRecordFactory
from typing import List

from sqlalchemy.orm import Session

from src.models.product import Product
from src.orm import RequestItemOrm
from src.orm.cart_orm import CartOrm, CartItemOrm
from src.models.cart import Cart
from src.orm.product_orm import ProductOrm
from src.repositories.base_repository import BaseRepository
from src.repositories.cart_item_repository import CartItemRepository


class CartRepository(BaseRepository[CartOrm, Cart]):
    def __init__(self, session: Session, cart_item_repository: CartItemRepository):
        self.session = session()
        self.cart_item_repository = cart_item_repository

    def get_by_id(self, id: int) -> Cart:
        orm_cart = self.session.query(CartOrm).filter(CartOrm.id == id).first()
        return Cart.model_validate(orm_cart, from_attributes=True)

    def get_all(self) -> List[Cart]:
        orm_carts = self.session.query(CartOrm).all()
        return [Cart.model_validate(cart, from_attributes=True) for cart in orm_carts]

    def create(self, entity: Cart) -> Cart:
        cart_orm = CartOrm(
            shop_id=entity.shop.id,
            user_id=entity.user_id,
            total_price=entity.total_price
        )
        self.session.add(cart_orm)
        self.session.flush()
        for item in entity.items:
            self.cart_item_repository.create(cart_id=cart_orm.id, entity=item)
        self.session.commit()
        self.session.refresh(cart_orm)
        return entity

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


