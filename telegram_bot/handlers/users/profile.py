from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.default.profile import profile_menu, back_to_profile
from keyboards.default.main_menu import create_main_menu, cancel_menu
from keyboards.inline.currency import currency_inline_menu

from datetime import datetime
from main import dp, bot
from db import get_users_wallets, create_wallet


class WalletForm(StatesGroup):
    """A form to input wallet data"""
    title = State()
    description = State()
    currency = State()


@dp.message_handler(Text(equals=['Кабінет', 'Назад до кабінету']))
async def show_profile(message: Message, state: FSMContext):
    """Profile"""

    await state.finish()
    await message.answer(
       text="Ви у власному кабінеті. Оберіть пункт меню", reply_markup=profile_menu
    )


@dp.message_handler(Text(equals=['Переглянути гаманці']))
async def show_users_wallets(message: Message):
    """Check all users wallets"""

    data, status_code = get_users_wallets(message.from_user.id)
    if status_code == 200:
        wallets = data['Wallets']
        if len(wallets) > 0:
            await message.answer(
               text="Ваші гаманці", reply_markup=back_to_profile
            )
            titles = [wallet.get('title') for wallet in wallets]
            await message.answer(
               text="\n".join(titles)
            )
        else:
            await message.answer(
                text="На разі, у Вас немає жодного гаманця. Створіть новий для використання"
            )
    elif status_code == 404:
        await message.answer(
            text="Ви не авторизовані. Пройдіть авторизацію, щоб отримати доступ до цього функціоналу",
            reply_markup=create_main_menu(auth=False)
        )
    else:
        await message.answer(
            text="Трапилася помилка. Спробуйте пізніше",
            reply_markup=create_main_menu(auth=False)
        )


@dp.message_handler(Text(equals=['Створити новий гаманець']))
async def process_creation_wallet(message: Message):
    """Create a new wallet"""
    await WalletForm.title.set()
    await message.answer(
        text="Введіть назву гаманця", reply_markup=cancel_menu
    )


@dp.message_handler(state=WalletForm.title)
async def get_wallet_title(message: Message, state: FSMContext):
    """
    Process wallet title
    """
    async with state.proxy() as data:
        data['title'] = str(message.text)
    await WalletForm.next()
    await message.answer("Введіть опис для гаманця")


@dp.message_handler(state=WalletForm.description)
async def get_wallet_description(message: Message, state: FSMContext):
    """
    Process wallet description
    """
    async with state.proxy() as data:
        data['description'] = str(message.text)
    await WalletForm.next()
    await message.answer("Оберіть валюту для гаманця", reply_markup=currency_inline_menu())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('currency'), state=WalletForm.currency)
async def process_callback_menu_currency(callback_query: CallbackQuery, state: FSMContext):
    call_data = callback_query.data
    telegram_id = callback_query.from_user.id

    async with state.proxy() as data:
        data['currency_code'] = str(call_data.split('_')[-1])

    wallet_data = {
        "title": data['title'],
        "description": data['description'],
        "basic_currency_code": data['currency_code'],
        "telegram_id": telegram_id,
    }

    response, status_code = create_wallet(wallet_data)
    if status_code == 201:
        await state.finish()
        await bot.send_message(chat_id=callback_query.from_user.id, text="Гаманець був успішно доданий", reply_markup=profile_menu)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Трапилася помилка. Спробуйте пізніше", reply_markup=profile_menu)