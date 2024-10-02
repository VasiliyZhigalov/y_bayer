import asyncio
import json

from playwright.async_api import async_playwright


async def intercept_api_calls(url):
    # С помощью sync_playwright можно запустить браузер
    async  with async_playwright() as p:
        # Запускаем Chromium браузер в headless режиме
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
        # Создаем новую страницу с заданным User-Agent
        context = await  browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        page = await  context.new_page()

        # Функция для блокировки ресурсов
        async def block_unnecessary(route):
            resource_type = route.request.resource_type
            if resource_type in ['stylesheet', 'font', 'image', 'media', 'script']:
                print(f"Блокировка {resource_type}: {route.request.url}")
                await route.abort()  # Блокируем ненужные ресурсы
            else:
                await route.continue_()

        # Перехватываем все запросы и блокируем ненужные типы ресурсов
        # await page.route("**/*", block_unnecessary)

        stop_loading = False

        # Функция для перехвата и блокировки дальнейших запросов
        async def block_request(route):
            nonlocal stop_loading
            if stop_loading:
                print(f"Запрос заблокирован: {route.request.url}")
                await route.abort()  # Прекращаем загрузку запроса
            else:
                await route.continue_()

        # Устанавливаем блокирование запросов
        # await page.route("**/*", block_request)
        api_product_request = None

        # Логирование запросов
        async def log_request(request):
            nonlocal api_product_request
            if "kuper.ru/api/web/v1/products" in request.url:
                api_product_request = request
                print(f"Перехваченный запрос: {request.url}")
                print(f"Метод: {request.method}")
                print(f"Заголовки: {request.headers}")
                print(
                    f"Параметры запроса: {request.post_data if request.method == 'POST' else request.url.split('?')[1] if '?' in request.url else ''}")

        # Логирование ответов
        async def log_response(response):
            nonlocal stop_loading
            # Ожидание полного получения тела ответа
            try:
                if "kuper.ru/api/web/v1/products" in response.url:
                    print(f"Перехваченный ответ: {response.url}")
                    print(f"Статус: {response.status}")
                    if "application/json" in response.headers.get("content-type", ""):
                        body = await response.json()  # Получение JSON-ответа
                        print(f"JSON ответ: {body}")
                    else:
                        body = await response.text()  # Текстовый ответ
                        print(f"Тело ответа (первые 100 символов): {body[:100]}")
                    stop_loading = True
            except Exception as e:
                print(f"Ошибка при получении тела ответа: {e}")

        page.on("response", log_response)
        page.on("request", log_request)

        # Переходим на целевую страницу
        await page.goto(url)
        await page.wait_for_timeout(7000)
        await page.click('input[type="text"]')
        await page.fill('input[type="text"]', '')
        await page.type('input[type="text"]', 'бананы' + '\n')
        await page.wait_for_timeout(4000)
        request_params = json.loads(api_product_request.post_data)
        # Меняем параметр 'q'
        request_params['q'] = 'бананы'

        # Шаг 3: Подготовить параметры POST-запроса
        request_params = {
            "store_id": "211",
            "page": "1",
            "per_page": "24",
            "tenant_id": "sbermarket",
            "q": "бананы",  # Меняем параметр q на 'бананы'
            "ads_identity": {
                "ads_promo_identity": {
                    "placement_uid": "cg4tmrigsvdveog2p240",
                    "site_uid": "c9qep2jupf8ugo3scn10"
                }
            },
            "filter": [
                {"key": "brand", "values": []},
                {"key": "permalinks", "values": []},
                {"key": "price", "values": []},
                {"key": "discounted", "values": []},
                {"key": "root_category", "values": []}
            ]
        }

        # Шаг 4: Подготовить заголовки для отправки POST-запроса
        custom_headers = {
            'sbm-forward-tenant': 'sbermarket',
            'sec-ch-ua-platform': '"Windows"',
            'x-csrf-token': '9hnD7pdf89hPTracnG080qq1HmhHU7gxv0KwdLTlRi6dk406xNWzHKspvQ18sbtfgxeSmSSNW+wmxBF7NdLY/Q==',
            'referer': 'https://kuper.ru/metro/search?ads_identity.ads_promo_identity.placement_uid=cg4tmrigsvdveog2p240&ads_identity.ads_promo_identity.site_uid=c9qep2jupf8ugo3scn10&anonymous_id=3000de88-5a97-4402-b592-37f86b83d473&keywords=%D0%B1%D0%B0%D0%BD%D0%B0%D0%BD%D1%8B&sid=211',
            'client-token': '7ba97b6f4049436dab90c789f946ee2f',
            'sec-ch-ua': '"HeadlessChrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'baggage': 'sentry-environment=client,sentry-release=r24-09-26-1400-7db5eb79,sentry-public_key=f9d0a0afb8d5420bb353a190580ae049,sentry-trace_id=35dd084efc3848c4ad3bfcb60050e9f0,sentry-sample_rate=0.1,sentry-transaction=%2F%5B...slugs%5D,sentry-sampled=false',
            'sentry-trace': '35dd084efc3848c4ad3bfcb60050e9f0-86b352e79c69b3b3-0',
            'anonymous_id': '3000de88-5a97-4402-b592-37f86b83d473',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json'
        }

        response = await page.request.post(
            url='https://kuper.ru/api/web/v1/products',
            headers=custom_headers,
            data=json.dumps(request_params)
        )
        # Шаг 6: Получить и вывести ответ
        if response.ok:
            await page.screenshot(path='screenshot.png', full_page=True)
            response_data = await response.json()
            print(f"Ответ от POST-запроса: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Ошибка: {response.status}")


        # Ожидаем загрузки контента и запросов
        await page.wait_for_timeout(100000)  # Ждем, чтобы запросы успели выполниться
        # Закрываем браузер
        await browser.close()


if __name__ == "__main__":
    # Пример вызова функции для конкретного URL сайта
    asyncio.run(intercept_api_calls('https://kuper.ru/metro/search?sid=211'))
