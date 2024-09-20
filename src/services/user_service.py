from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:
        """
        Получает данные пользователя по ID.

        :param user_id: ID пользователя
        :return: Данные пользователя
        """
        return self.user_repository.get(user_id)

    def create_user(self, user: User) -> User:
        """
        Создает нового пользователя.

        :param user: Данные пользователя
        :return: Созданный пользователь
        """
        if self.user_repository.get_by_id(user.id) is None:
            self.user_repository.create(user)
        return user
