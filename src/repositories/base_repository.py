from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar('T')
U = TypeVar('U')


class BaseRepository(ABC, Generic[T, U]):
    @abstractmethod
    def get_by_id(self, id: int) -> U:
        pass


    @abstractmethod
    def get_all(self) -> List[U]:
        pass

    @abstractmethod
    def create(self, entity: U) -> U:
        pass

    @abstractmethod
    def update(self, id: int, entity: U) -> U:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
