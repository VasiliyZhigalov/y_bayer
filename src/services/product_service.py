from typing import List

from src.models.product import Product
from src.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def find_products(self, search_query: str) -> List[Product]:
        """
        Ищет продукты по запросу.

        :param search_query: Строка поиска
        :return: Список продуктов
        """
        return self.product_repository.find_by_name(search_query)

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Получает данные продукта по ID.

        :param product_id: ID продукта
        :return: Данные продукта
        """
        return self.product_repository.get(product_id)
