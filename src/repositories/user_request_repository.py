from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
from typing import List

from src.orm import UserRequestOrm, RequestItemOrm
from src.models.user_request import UserRequest
from src.repositories.base_repository import BaseRepository


class UserRequestRepository(BaseRepository[UserRequestOrm, UserRequest]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> UserRequest:
        orm_request = self.session.query(UserRequestOrm).filter(UserRequestOrm.id == id).first()
        return UserRequest.model_validate(orm_request, from_attributes=True)

    def get_all(self) -> List[UserRequest]:
        orm_request = self.session.query(UserRequestOrm).all()
        return [UserRequest.model_validate(request, from_attributes=True) for request in orm_request]

    def create(self, entity: UserRequest) -> UserRequest:
        orm_items = [RequestItemOrm(product_name=item.product_name, quantity=item.quantity) for item in entity.items]

        orm_request = UserRequestOrm(
            user_id=entity.user_id,
            items=orm_items
        )
        self.session.add(orm_request)
        self.session.commit()
        self.session.refresh(orm_request)
        return UserRequest.model_validate(orm_request, from_attributes=True)

    def update(self, id: int, entity: UserRequest) -> UserRequest:
        orm_request = self.session.query(UserRequestOrm).filter(UserRequestOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_request, key, value)
        self.session.commit()
        return UserRequest.model_validate(orm_request, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_request = self.session.query(UserRequestOrm).filter(UserRequestOrm.id == id).first()
        self.session.delete(orm_request)
        self.session.commit()

    def get_by_user_id(self, user_id: int) -> UserRequest:
        orm_request = self.session.query(UserRequestOrm).filter(UserRequestOrm.user_id == user_id).first()
        return UserRequest.model_validate(orm_request, from_attributes=True)

    def clear(self) -> None:
        for orm_request in self.session.query(UserRequestOrm).all():
            self.session.delete(orm_request)
        self.session.commit()
