from aiogram.filters.command import Command
from aiogram import types, Router
from dependency_injector.wiring import inject, Provide

from src.containers import AppContainer
from src.models.shop import Shop
from src.models.user import User
from src.models.user_request import UserRequest, RequestItem
from src.services import user_request_service
from src.services.cart_service import CartService
from src.services.product_service import ProductService
from src.services.scraping_service import ScrapingService
from src.services.telegram_service import TelegramService
from src.services.user_request_service import UserRequestService
from src.services.user_service import UserService
from src.utils import parse_shopping_list

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message):
    """
    Обработчик команды /start. Приветствует пользователя и предлагает ввести список покупок.
    """
    await message.reply(
        "Привет! Я бот-помощник для покупок на Купер. Отправь мне список покупок, и я найду лучшие цены для тебя!")


@router.message(Command('help'))
async def help_command(message: types.Message):
    """
    Обработчик команды /help. Показывает справку по использованию бота.
    """
    help_text = (
        "Я помогу тебе найти лучшие предложения для твоего списка покупок. "
        "Просто отправь мне список товаров через запятую, и я покажу, где можно купить их по лучшей цене."
    )
    await message.reply(help_text)


@router.message()
@inject
async def handle_shopping_list(
        message: types.Message,
        user_service: UserService = Provide[AppContainer.user_service],
        scraping_service: ScrapingService = Provide[AppContainer.scraping_service],
        product_service: ProductService = Provide[AppContainer.product_service],
        cart_service: CartService = Provide[AppContainer.cart_service],
        telegram_service: TelegramService = Provide[AppContainer.telegram_service],
        user_request_service: UserRequestService = Provide[AppContainer.user_request_service]
):
    """
    Обработчик текста сообщения, предполагая, что это список покупок.
    Парсит список и запускает процесс поиска товаров.
    """
    user_id = message.from_user.id
    user = User(id=user_id, name=message.from_user.first_name)
    user_service.create_user(user)

    shopping_list = parse_shopping_list(message.text)
    if not shopping_list:
        await message.reply("Не удалось распознать продукты. Пожалуйста, попробуйте ввести список еще раз.")
        return

    # Создание запроса пользователя
    new_user_request = UserRequest(user_id=user_id)
    for item in shopping_list:
        request_item = RequestItem(product_name=item['name'], quantity=item['quantity'])
        new_user_request.items.append(request_item)
    user_request_service.clear()
    user_request_service.create_request(new_user_request)
    user_request = user_request_service.get_requests(user_id)
    await telegram_service.send_user_request(user_id, user_request)

    # Парсинг данных из магазинов
    metro = Shop(id=1, name='Metro', url='https://kuper.ru/metro/search?sid=211')
    carts = await scraping_service.fetch_products([metro], user_request)

    # Отображение пользователю вариантов корзин
    await telegram_service.show_carts(user_id, carts)
