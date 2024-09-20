import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/products']

    def parse(self, response):
        for product in response.css('div.product'):
            yield {
                'name': product.css('a::text').get(),
                'price': product.css('span.price::text').get(),
                'link': response.urljoin(product.css('a::attr(href)').get()),
            }

