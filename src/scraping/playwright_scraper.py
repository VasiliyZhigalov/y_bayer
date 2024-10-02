import asyncio
from itertools import product
from typing import List

from src.models.cart import Cart, CartItem
from src.models.product import Product
from src.models.user_request import UserRequest, RequestItem
from src.scraping.base_scraper import BaseScraper
from playwright.async_api import async_playwright


class PlaywrightScraper(BaseScraper):
    def __init__(self):
        self.stop_loading = False
        self.response_body = None

    async def fetch_product(self, shop_url, user_request: UserRequest) -> List[CartItem]:
        print("Стаpт парсинга")
        cart_items = []
        async with async_playwright() as p:
            page = await self._setup_browser(p, shop_url)
            page.on("response", self._get_response_body)
            for item in user_request.items:
                await self._search_product(page, item.product_name)
                product = self.response_body['products'][0]  # Сделать проброс ошибок
                cart_item = self._create_cart_item(product, item)
                cart_items.append(cart_item)
        return cart_items

    async def _setup_browser(self, p, shop_url):
        browser = await p.chromium.launch(headless=True, args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--window-size=1920,1080',
            '--disable-extensions',
            '--disable-popup-blocking',
            '--disable-translate',
            '--disable-gpu'
        ])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = await context.new_page()
        await page.route("**/*", self._block_request)
        await page.goto(shop_url)
        return page

    async def _search_product(self, page, product_name):
        await page.wait_for_timeout(7000)
        await page.click('input[type="text"]')
        await page.fill('input[type="text"]', '')
        await page.type('input[type="text"]', str(product_name) + '\n')
        await page.wait_for_timeout(7000)

    def _create_cart_item(self, product_data, request_item):
        product = Product(
            name=product_data['name'],
            request_product_name=request_item.product_name,
            price=product_data['price'],
            human_volume=product_data['human_volume'],
            volume=product_data['volume'],
            volume_type=product_data['volume_type'],
            price_type=product_data['price_type'],
            slug=product_data['slug'],
            sku=product_data['sku'],
            image_urls=product_data['image_urls'][0],
            canonical_url=product_data['canonical_url']
        )
        return CartItem(quantity=request_item.quantity, request_product_name=request_item.product_name, product=product)

    async def _get_response_body(self, response):
        try:
            if "kuper.ru/api/web/v1/products" in response.url:
                if "application/json" in response.headers.get("content-type", ""):
                    self.response_body = await response.json()
                else:
                    self.response_body = await response.text()
        except Exception as e:
            print(f"Ошибка при получении тела ответа: {e}")

    async def _block_request(self, route):
        # Вынесен блок запросов
        if self.stop_loading:
            await route.abort()
        else:
            await route.continue_()


"""
    async def fetch_product(self, shop_url, user_requesr: UserRequest) -> List[CartItem]:
        response_body = None
        stop_loading = False

        async def get_response_body(response):
            '''
            Колл бек функция для фильтрации запросов на продукты
            :param response:
            :return:
            '''
            nonlocal response_body, stop_loading
            try:
                if "kuper.ru/api/web/v1/products" in response.url:
                    print(f"Перехваченный ответ: {response.url}")
                    if "application/json" in response.headers.get("content-type", ""):
                        response_body = await response.json()  # Получение JSON-ответа
                    #   print(f"JSON ответ: {response_body}")
                    else:
                        response_body = await response.text()  # Получение текстового ответа
                        # print(f"Тело ответа (первые 100 символов): {response_body[:100]}")
                    # stop_loading = True
            except Exception as e:
                print(f"Ошибка при получении тела ответа: {e}")

        # Функция для перехвата и блокировки дальнейших запросов
        async def block_request(route):
            nonlocal stop_loading
            if stop_loading:
                print(f"Запрос заблокирован: {route.request.url}")
                await route.abort()  # Прекращаем загрузку запроса
            else:
                await route.continue_()

        async with async_playwright() as p:
            browser = await  p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable - setuid - sandbox',
                '--disable-infobars',
                '--window-size=1920,1080',
                '--disable - extensions',
                '--disable-popup-blocking',
                '--disable-infobars',
                '--disable-translate',
                '--disable-gpu'
            ])
            context = await  browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await  context.new_page()
            page.on("response", get_response_body)
            # Устанавливаем перехват запросов
            await page.route("**/*", block_request)

            cart_items = []
            await page.goto(shop_url)
            for item in user_requesr.items:
                stop_loading = False
                await page.wait_for_timeout(7000)
                await page.click('input[type="text"]')
                await page.fill('input[type="text"]', '')
                await page.type('input[type="text"]', str(item.product_name) + '\n')
                await page.wait_for_timeout(4000)
                p = response_body['products'][0]

                product = Product(
                    name=p['name'],  # название
                    request_product_name=item.product_name,  # запрос,
                    price=p['price'],  # цена
                    human_volume=p['human_volume'],  # объем товара в понятной для покупателя форме.
                    volume=p['volume'],  # объем товара
                    volume_type=p['volume_type'],  # тип объема
                    price_type=p['price_type'],  # тип цены, указывающий, что цена указана за килограмм
                    slug=p['slug'],  # удобный для чтения идентификатор, используемый в URL
                    sku=p['sku'],  # код товара для магазина.
                    image_urls=p['image_urls'][0],  # массив URL-адресов изображений товара
                    canonical_url=p['canonical_url']  # ссылка на страницу товара в магазине
                )
                it = CartItem(quantity=item.quantity, product=product)
            cart_items.append(it)
            return cart_items


if __name__ == "__main__":
    scraper = PlaywrightScraper()
    item = RequestItem(product_name="соль", quantity=1)
    item1 = RequestItem(product_name="бананы", quantity=1)
    user_request = UserRequest(user_id=1)
    user_request.items.append(item)
    user_request.items.append(item1)
    cart_items = asyncio.run(scraper.fetch_product("https://kuper.ru/metro/search?sid=211", user_request))
    print(str(cart_items))
"""
