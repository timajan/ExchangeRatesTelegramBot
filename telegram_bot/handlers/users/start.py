from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.default.main_menu import create_main_menu, back_menu, cancel_menu

from datetime import datetime
from main import dp
from db import get_rates, get_user


class RatesForm(StatesGroup):
    """A form to input rate date"""
    date = State("")


@dp.message_handler(Command('start') | Text(equals=['Назад до старту']), state='*')
async def show_menu(message: Message, state: FSMContext):
    """Start"""
    await state.reset_state()
    user, status_code = get_user(telegram_id=message.from_user.id)
    if status_code == 200:
        auth = True
    else:
        auth = False
    await message.answer(
       text="Вітаю! Оберіть пункт меню", reply_markup=create_main_menu(auth)
    )


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Відміна', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Allow user to cancel any action
    """

    await state.finish()
    user, status_code = get_user(message.from_user.id)
    auth = True if status_code == 200 else False
    await message.answer('Відмінено', reply_markup=create_main_menu(auth=auth))


@dp.message_handler(Text(equals="Отримати список курс"))
async def get_rate_date(message: Message):

    await RatesForm.date.set()

    await message.answer(
        text="Введіть дату курсу валют у форматі dd.mm.YYYY", reply_markup=cancel_menu
    )


@dp.message_handler(state=RatesForm.date)
async def get_rates_list(message: Message, state: FSMContext):
    date_format = "%d.%m.%Y"
    date_string = message.text

    try:
        datetime_object = datetime.strptime(date_string, date_format)
    except ValueError:
        await message.answer("Введіть правильний формат дати. dd.mm.YYYY")
        return

    today = datetime.today()
    if datetime_object > today:
        await message.answer("Введіть дату до сьогоднішнього дня")
        return

    async with state.proxy() as date:
        date['date'] = message.text

    data, status_code = get_rates(date['date'])

    if status_code == 200:
        currency_rates = []
        for entry in data["exchangeRate"]:
            currency = entry['currency']
            rate = entry['saleRateNB']  # You can change to 'purchaseRateNB' or any other rate you prefer
            currency_rates.append(f"{currency}: {rate}")

        await message.answer("\n".join(currency_rates), reply_markup=back_menu)
    else:
        await message.answer("Трапилася помилка", reply_markup=back_menu)

