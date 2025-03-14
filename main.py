from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import user_handlers
from keyboards.set_menu import set_main_menu
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[{asctime}] #{levelname} >> {message} << {filename} | '
                           'line {lineno} | {name}',
                    style='{'
                    )
logger = logging.getLogger(__name__)


async def start():

    config = load_config()
    token = config.tgbot.token

    bot = Bot(token=token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())
