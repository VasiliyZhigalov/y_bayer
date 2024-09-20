from dependency_injector import containers, providers

from aiogram import Bot, Dispatcher

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UserRepository
from src.repositories.user_request_repository import UserRequestRepository
from src.services.cart_service import CartService
from src.services.product_service import ProductService
from src.services.scraping_service import ScrapingService
from src.services.telegram_service import TelegramService
from src.services.user_request_service import UserRequestService
from src.services.user_service import UserService


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()  # Провайдер конфигурации

    bot = providers.Singleton(Bot, token='6879369889:AAHV4OlIswC_pEITX18r1h3_lwIzC6Jyv0E')
    dispatcher = providers.Singleton(Dispatcher, bot=bot)

    engine = providers.Singleton(create_engine, url='sqlite:///shop_assistant.db', echo=False)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    user_repository = providers.Singleton(UserRepository, session=session_factory)
    cart_repository = providers.Singleton(CartRepository, session=session_factory)
    product_repository = providers.Singleton(ProductRepository, session=session_factory)
    user_request_repository = providers.Singleton(UserRequestRepository, session=session_factory)

    user_service = providers.Singleton(UserService, user_repository=user_repository)
    cart_service = providers.Singleton(CartService, cart_repository=cart_repository)
    product_service = providers.Singleton(ProductService, product_repository=product_repository)
    telegram_service = providers.Singleton(TelegramService, bot=bot, dp=dispatcher)
    user_request_service = providers.Singleton(UserRequestService, user_request_repository=user_request_repository)

    scraping_service = providers.Factory(ScrapingService)
