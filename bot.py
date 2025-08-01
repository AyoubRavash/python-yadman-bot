import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import common


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(common.router)

    print('Bot started.')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
