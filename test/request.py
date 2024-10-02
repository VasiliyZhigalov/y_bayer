import asyncio

from playwright.async_api import async_playwright

api_request = None


class Req:
    def __init__(self):
        self.api_request = None

    async def search_product(self, page, product_name):
        # Логика поиска продукта в магазине
        await page.wait_for_timeout(7000)
        await page.click('input[type="text"]')
        await page.fill('input[type="text"]', '')
        await page.type('input[type="text"]', str(product_name) + '\n')
        await page.wait_for_timeout(7000)


    async def callback_request_api(self,request):
        print("{{{}}}")
        if "kuper.ru/api/web/v1/products" in request.url:
            self.api_reqest = request
            print(f"Перехваченный запрос: {request.url}")
            print(f"Метод: {request.method}")
            print(f"Заголовки: {request.headers}")
            print(
                f"Параметры запроса: {request.post_data if request.method == 'POST' else request.url.split('?')[1] if '?' in request.url else ''}")


    async def setup_browser(self,p, shop_url):
        # Вынесли настройку браузера и обработку запросов
        browser = await p.chromium.launch(headless=False, args=[
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
        await page.goto(shop_url)
        return page


    async def main(self,url):
        async with async_playwright() as p:
            page = await self.setup_browser(p, url)
            await self.search_product(page, "банан")
            page.on("request", self.callback_request_api)
            api_r = self.api_request


if __name__ == "__main__":
    r = Req()
        # Пример вызова функции для конкретного URL сайта
    asyncio.run(r.main('https://kuper.ru/metro/search?sid=211'))
