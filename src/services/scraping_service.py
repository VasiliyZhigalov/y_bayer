from typing import List, Dict

class ScrapingService:
    def __init__(self):
        # Инициализация сервисов, если необходимо
        pass

    def fetch_products(self, shop_urls: List[str], user_request: Dict[str, int]) -> Dict[str, List[Dict]]:
        """
        Парсит данные о товарах из указанных URL магазинов и сопоставляет их с запросом пользователя.

        :param shop_urls: Список URL магазинов для парсинга
        :param user_request: Словарь с товарами и их количеством из запроса пользователя
        :return: Словарь с данными о товарах из каждого магазина
        """
        results = {}
        for url in shop_urls:
            # Логика парсинга с использованием Scrapy
            # Заполняем results данными о товарах из магазинов
            pass

        return results
