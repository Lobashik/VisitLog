from aiogram import Bot, Dispatcher

from app.config import settings
from app.handlers.base import router


bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("/app/logs/bot_log.log", mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    import asyncio
    asyncio.run(main())
