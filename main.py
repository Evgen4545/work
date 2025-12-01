# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from database import create_tables
from bot import register_handlers

# Настройки
API_TOKEN = 'YOU_TOKEN'  # Замените на свой токен

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Инициализация БД
    await create_tables()

    # Регистрация обработчиков
    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
