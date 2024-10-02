from sqlalchemy.orm import Session
from typing import List

from src.models.product import Product
from src.orm.cart_orm import CartItemOrm
from src.models.cart import CartItem as CartItem
from src.orm.product_orm import ProductOrm
from src.repositories.base_repository import BaseRepository


class CartItemRepository(BaseRepository[CartItemOrm, CartItem]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> CartItem:
        orm_cart_item = self.session.query(CartItemOrm).filter(CartItemOrm.id == id).first()
        return CartItem.model_validate(orm_cart_item, from_attributes=True)

    def get_all(self) -> List[CartItem]:
        orm_cart_items = self.session.query(CartItemOrm).all()
        return [CartItem.model_validate(cart_item, from_attributes=True) for cart_item in orm_cart_items]

    def create(self, entity: CartItem, cart_id: int) -> CartItemOrm:
        orm_product = self._create_product(entity.product)
        orm_cart_item = CartItemOrm(
            cart_id=cart_id,
            quantity=entity.quantity,
            request_product_name=entity.request_product_name,
            product=orm_product.id
        )
        self.session.add(orm_cart_item)
        self.session.flush()
        self.session.commit()
        return orm_cart_item

    def update(self, id: int, entity: CartItem) -> CartItem:
        orm_cart_item = self.session.query(CartItemOrm).filter(CartItemOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_cart_item, key, value)
        self.session.commit()
        return CartItem.model_validate(orm_cart_item, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_cart_item = self.session.query(CartItemOrm).filter(CartItemOrm.id == id).first()
        self.session.delete(orm_cart_item)
        self.session.commit()

    def _create_product(self, product: Product) -> ProductOrm:
        product_orm = ProductOrm(**product.model_dump())
        self.session.add(product_orm)
        self.session.flush()
        self.session.commit()
        return product_orm
