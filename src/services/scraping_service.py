import asyncio
from typing import List, Dict

from src.models.cart import Cart
from src.models.shop import Shop
from src.models.user_request import UserRequest
from src.repositories.cart_repository import CartRepository
from src.scraping.base_scraper import BaseScraper


class ScrapingService:
    def __init__(self, scraper: BaseScraper, cart_repository: CartRepository):
        self.scraper = scraper
        self.cart_repository = cart_repository

    async def fetch_products(self, shops: List[Shop], user_request: UserRequest) -> List[Cart]:
        """
        Парсит данные о товарах из указанных URL магазинов и сопоставляет их с запросом пользователя.

        :param shop: Список магазинов для парсинга
        :param user_request: Словарь с товарами и их количеством из запроса пользователя
        :return: Список корзин с товарами
        :rtype: List[Cart]
        """
        carts = []
        for shop in shops:
            cart_items = await self.scraper.fetch_product(shop.url, user_request)
            cart = Cart(shop=shop, user_id=user_request.user_id, items=cart_items)
            self.cart_repository.create(cart)
            carts.append(cart)
        return carts
