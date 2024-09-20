from typing import List, Dict

from aiogram import Bot, Dispatcher, types

from src.models.user_request import UserRequest


class TelegramService:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    async def send_message(self, chat_id: int, text: str):
        """
        Отправляет сообщение пользователю.

        :param chat_id: ID чата пользователя
        :param text: Текст сообщения
        """
        await self.bot.send_message(chat_id, text)

    async def show_user_request(self, chat_id: int, request: UserRequest):
        request_str = ''
        for pr in request:
            request_str = +pr
        await self.bot.send_message(chat_id, request_str)

    async def send_user_request(self, chat_id: str, user_request: UserRequest) -> None:
        # Формирование сообщения
        items_message = "\n".join(
            [f"{item.product_name} - {item.quantity}" for item in user_request.items]
        )
        message = f"Ваш заказ:\n{items_message}\n\nПодтвердите заказ, нажав на кнопку ниже."

        # Создание инлайн-кнопки
        keyboard = [
            list([types.InlineKeyboardButton(text="Подтвердить список", callback_data=f"confirm_{user_request.id}")]),
        ]
        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)

        # Отправка сообщения
        await self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    async def show_cart_options(self, chat_id: int, carts: List[Dict]):
        """
        Отображает кнопки с корзинами пользователя.

        :param chat_id: ID чата пользователя
        :param carts: Список корзин для отображения
        """
        if len(carts) == 0:
            await self.bot.send_message(chat_id, "Нет доступных корзин")
            return
        buttons = []
        for cart in carts:
            button = types.InlineKeyboardButton(cart["shop_name"], callback_data=f"cart_{cart['id']}")
        markup = self.ease_link_kb()
        await self.bot.send_message(chat_id, "Выберите корзину:", reply_markup=markup)
