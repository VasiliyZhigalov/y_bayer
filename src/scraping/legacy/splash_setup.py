from scrapy_splash import SplashRequest

def parse(self, response):
    yield SplashRequest(
        url='http://example.com',
        callback=self.parse_result,
        args={'wait': 2, 'images': 0},
    )
