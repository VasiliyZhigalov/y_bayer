from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
from typing import List

from src.containers import AppContainer
from src.orm.user_request_orm import RequestItemOrm
from src.models.user_request import RequestItem
from src.repositories.base_repository import BaseRepository


class RequestItemRepository(BaseRepository[RequestItemOrm, RequestItem]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> RequestItem:
        orm_request_item = self.session.query(RequestItemOrm).filter(RequestItemOrm.id == id).first()
        return RequestItem.model_validate(orm_request_item, from_attributes=True)

    def get_all(self) -> List[RequestItem]:
        orm_request_items = self.session.query(RequestItemOrm).all()
        return [RequestItem.model_validate(request_item, from_attributes=True) for request_item in orm_request_items]

    def create(self, entity: RequestItem) -> RequestItem:
        orm_request_item = RequestItemOrm(**entity.dict())
        self.session.add(orm_request_item)
        self.session.commit()
        self.session.refresh(orm_request_item)
        return RequestItem.model_validate(orm_request_item, from_attributes=True)

    def update(self, id: int, entity: RequestItem) -> RequestItem:
        orm_request_item = self.session.query(RequestItemOrm).filter(RequestItemOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_request_item, key, value)
        self.session.commit()
        return RequestItem.model_validate(orm_request_item, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_request_item = self.session.query(RequestItemOrm).filter(RequestItemOrm.id == id).first()
        self.session.delete(orm_request_item)
        self.session.commit()
