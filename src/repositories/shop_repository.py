from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
from typing import List
from src.containers import AppContainer
from src.orm.shop_orm import ShopOrm
from src.models.shop import Shop
from src.repositories.base_repository import BaseRepository


class ShopRepository(BaseRepository[ShopOrm, Shop]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> Shop:
        orm_shop = self.session.query(ShopOrm).filter(ShopOrm.id == id).first()
        return Shop.model_validate(orm_shop, from_attributes=True)

    def get_all(self) -> List[Shop]:
        orm_shops = self.session.query(ShopOrm).all()
        return [Shop.model_validate(shop, from_attributes=True) for shop in orm_shops]

    def create(self, entity: Shop) -> Shop:
        orm_shop = ShopOrm(**entity.dict())
        self.session.add(orm_shop)
        self.session.commit()
        self.session.refresh(orm_shop)
        return Shop.model_validate(orm_shop, from_attributes=True)

    def update(self, id: int, entity: Shop) -> Shop:
        orm_shop = self.session.query(ShopOrm).filter(ShopOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_shop, key, value)
        self.session.commit()
        return Shop.model_validate(orm_shop, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_shop = self.session.query(ShopOrm).filter(ShopOrm.id == id).first()
        self.session.delete(orm_shop)
        self.session.commit()

