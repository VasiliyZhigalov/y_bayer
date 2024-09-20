from typing import List
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from src.orm import UserOrm,UserRequestOrm

from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserOrm, User]):
    def __init__(self, session: Session):
        self.session = session()

    def get_by_id(self, id: int) -> User:
        orm_user = self.session.query(UserOrm).filter(UserOrm.id == id).first()
        if orm_user is None:
            return None
        return User.model_validate(orm_user, from_attributes=True)

    def get_all(self) -> List[User]:
        orm_users = self.session.query(UserOrm).all()
        return [User.model_validate(user, from_attributes=True) for user in orm_users]

    def create(self, entity: User) -> User:
        try:
            orm_user = UserOrm(**entity.model_dump())
            self.session.add(orm_user)
            self.session.commit()
            self.session.refresh(orm_user)
        except IntegrityError:
            self.session.rollback()
            raise
        return User.model_validate(orm_user, from_attributes=True)

    def update(self, id: int, entity: User) -> User:
        orm_user = self.session.query(UserOrm).filter(UserOrm.id == id).first()
        for key, value in entity.dict().items():
            setattr(orm_user, key, value)
        self.session.commit()
        return User.model_validate(orm_user, from_attributes=True)

    def delete(self, id: int) -> None:
        orm_user = self.session.query(UserOrm).filter(UserOrm.id == id).first()
        self.session.delete(orm_user)
        self.session.commit()


