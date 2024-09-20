from sqlalchemy.orm import Session
from typing import List

from src.orm.product_orm import ProductOrm
from src.models.product import Product
from src.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[ProductOrm, Product]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> Product:
        orm_product = self.session.query(ProductOrm).filter(ProductOrm.id == id).first()
        return Product.model_validate(orm_product, from_attributes=True)

    def get_all(self) -> List[Product]:
        orm_products = self.session.query(ProductOrm).all()
        return [Product.model_validate(product, from_attributes=True) for product in orm_products]

    def create(self, entity: Product) -> Product:
        orm_product = ProductOrm(**entity.dict())
        self.session.add(orm_product)
        self.session.commit()
        self.session.refresh(orm_product)
        return Product.model_validate(orm_product, from_attributes=True)

    def update(self, id: int, entity: Product) -> Product:
        orm_product = self.session.query(ProductOrm).filter(ProductOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_product, key, value)
        self.session.commit()
        return Product.model_validate(orm_product, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_product = self.session.query(ProductOrm).filter(ProductOrm.id == id).first()
        self.session.delete(orm_product)
        self.session.commit()
