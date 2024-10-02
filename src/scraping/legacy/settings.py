# scraping/settings.py

# Настройки Scrapy
BOT_NAME = 'your_bot_name'
SPIDER_MODULES = ['your_project.spiders']
NEWSPIDER_MODULE = 'your_project.spiders'

# Настройки для Splash
SPLASH_URL = 'http://localhost:8050'  # URL вашего Splash-сервера

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
