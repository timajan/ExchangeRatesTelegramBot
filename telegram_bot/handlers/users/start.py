from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ContentType

from keyboards.default.main_menu import main_menu

from main import dp
from db import get_rates


@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    """Start"""
    await message.answer(
       text="Hello", reply_markup=main_menu
    )


@dp.message_handler(Text(equals="Отримати список курс"))
async def get_rates_list(message: Message):
    date = "01.12.2014"
    data = get_rates(date)
    currency_rates = []
    for entry in data["exchangeRate"]:
        currency = entry['currency']
        rate = entry['saleRateNB']  # You can change to 'purchaseRateNB' or any other rate you prefer
        currency_rates.append(f"{currency}: {rate}")

    await message.answer(
        text="\n".join(currency_rates)
    )
