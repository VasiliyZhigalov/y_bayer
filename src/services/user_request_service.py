from src.models.user_request import UserRequest
from src.repositories.user_request_repository import UserRequestRepository


class UserRequestService:
    def __init__(self, user_request_repository: UserRequestRepository):
        self.user_request_repository = user_request_repository

    def create_request(self, user_request: UserRequest) -> UserRequest:
        return self.user_request_repository.create(user_request)

    def get_request(self, request_id) -> UserRequest:
        # Получение запроса по ID
        return self.user_request_repository.get_user_request_by_id(request_id)

    def get_requests(self, user_id):
        # Получение всех запросов пользователя
        return self.user_request_repository.get_by_user_id(user_id)

    def update_request(self, request_id, new_data):
        # Обновление существующего запроса
        request = self.get_request(request_id)
        if request:
            request.request_data = new_data
            self.user_request_repository.update_user_request(request)
            return request
        return None

    def delete_request(self, request_id):
        # Удаление запроса пользователя
        return self.user_request_repository.delete_user_request(request_id)

    def clear(self):
        return self.user_request_repository.clear()
