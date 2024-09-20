
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token='6879369889:AAHV4OlIswC_pEITX18r1h3_lwIzC6Jyv0E')
# Диспетчер
dp = Dispatcher()

def ease_link_kb():
    inline_kb_list = [
        [types.InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [types.InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!",reply_markup =ease_link_kb())

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
