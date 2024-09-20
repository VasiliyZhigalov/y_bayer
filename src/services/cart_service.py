from typing import List

from src.models.cart import Cart, CartItem
from src.repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def create_cart(self, user_id: int, shop_id: int, items: List[CartItem]) -> Cart:
        """
        Создает корзину для пользователя.

        :param user_id: ID пользователя
        :param shop_id: ID магазина
        :param items: Список товаров в корзине
        :return: Созданная корзина
        """
        total_price = sum(item.quantity * item.price for item in items)
        cart = Cart(user_id=user_id, shop_id=shop_id, items=items, total_price=total_price)
        self.cart_repository.create(cart)
        return cart

    def update_cart(self, cart_id: int, items: List[CartItem]) -> Cart:
        """
        Обновляет корзину с новыми товарами.

        :param cart_id: ID корзины
        :param items: Обновленный список товаров
        :return: Обновленная корзина
        """
        cart = self.cart_repository.get_by_id(cart_id)
        cart.items = items
        cart.total_price = sum(item.quantity * item.price for item in items)
        self.cart_repository.create(cart)
        return cart
