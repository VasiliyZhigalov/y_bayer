from abc import ABC, abstractmethod

from src.models.cart import Cart
from src.models.user_request import UserRequest


class BaseScraper(ABC):

    @abstractmethod
    def fetch_product(shop_url, user_requesr:UserRequest) -> Cart:
        pass