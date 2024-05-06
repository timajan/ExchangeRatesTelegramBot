import logging
from aiogram import Bot, Dispatcher, types
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token="6491433399:AAEvvaXsDVDGsdTAOCNmVu9POKuXyZcGvMM", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


async def on_shutdown():
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown)
