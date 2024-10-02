from aiogram.filters.command import Command
from aiogram import types, Router
import importlib
import pkgutil
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.scraping.legacy.scraper import ProductSpider

from src import repositories, orm, services, models, views
from src.api import bot_handlers


def reload_package(package):
    # Перебор всех модулей в пакете
    for module_info in pkgutil.iter_modules(package.__path__):
        module_name = f"{package.__name__}.{module_info.name}"
        if module_name in sys.modules:
            # Перезагрузка модуля, если он уже загружен
            importlib.reload(sys.modules[module_name])


service_router = Router()


@service_router.message(Command("reload"))
async def reload_modules(message: types.Message):
    '''
    Перезагрузка модулей бота
    :param message:
    :return:
    '''
    reload_package(repositories)
    reload_package(services)
    reload_package(models)
    reload_package(orm)
    reload_package(views)
    importlib.reload(bot_handlers)
    print("Модули успешно перезагружены!")
    await message.answer("Модули успешно перезагружены!")


@service_router.message(Command("scrapy"))
async def start_scrapy(message: types.Message):
    '''
    Запуск скрапера
    :param message:
    :return:
    '''
    await message.answer("Запуск парсинга...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(ProductSpider)
    process.start()

    await message.answer("Парсинг завершён. Результаты сохранены.")
