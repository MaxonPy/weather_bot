import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import logging

from app.handlers import router

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
