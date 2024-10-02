import scrapy
from scrapy_splash import SplashRequest


class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/85.0.4183.121 Safari/537.36',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',

    }

    allowed_domains = ['kuper.ru','localhost']
    start_urls = [
        'https://kuper.ru/metro/search?ads_identity.ads_promo_identity.placement_uid=cg4tmrigsvdveog2p240&ads_identity.ads_promo_identity.site_uid=c9qep2jupf8ugo3scn10&anonymous_id=78d0306e-09d4-4210-bec7-060fe9338e91&keywords=бананы%20фрукты&sid=211']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.lua_script,
                    'timeout': 90,
                    'wait': 2,
                },
                headers={
                    'User-Agent': self.settings.get('USER_AGENT'),
                },
                splash_headers={
                    'User-Agent': self.settings.get('USER_AGENT'),
                },
            )

    lua_script = """
        function main(splash)
            splash:set_user_agent(splash.args.headers['User-Agent'])
            splash:on_request(function(request)
                request:set_header('User-Agent', splash.args.headers['User-Agent'])
            end)
            assert(splash:go{splash.args.url, headers=splash.args.headers})
            splash:wait(splash.args.wait)
            return {
                html = splash:html(),
            }
        end
        """

    def parse(self, response):
        if response.status == 403:
            self.logger.error('Доступ запрещен: 403 Forbidden')
            return

        products = response.css('.ProductCard_root__zO_B9')  # Предположим, что у вас есть класс 'product'
        for product in products:
            print(product.css('.ProductCard_title__iB_Dr::text').get())
            yield {
                'name': product.css('.ProductCard_title__iB_Dr::text').get(),
                'price': product.css(
                    '.ProductCardPrice_price__zSwp0 ProductCardPrice_accent__6BZDJ CommonProductCard_priceText__S5e9l').get(),
                'url': response.css(".Link_root__4y_Mz Link_disguised__1Avt5 ProductCardLink_root__38cOL").get,
            }
