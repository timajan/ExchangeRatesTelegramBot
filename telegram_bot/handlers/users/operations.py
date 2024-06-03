from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline.operations import create_wallet_list_menu
from keyboards.default.profile import profile_menu
from keyboards.default.main_menu import cancel_menu
from db import to_up, to_down, get_currency, get_wallet, transfer, delete_wallet
from main import dp


@dp.message_handler(Text(equals="Поповнити"))
async def to_up_bill(message: Message):
    """"""

    telegram_id = message.from_user.id

    await message.answer(
        text="Оберіть гаманець", reply_markup=create_wallet_list_menu(telegram_id, "to_up")
    )


@dp.message_handler(Text(equals="Списати"))
async def to_down_bill(message: Message):
    """"""

    telegram_id = message.from_user.id

    await message.answer(
        text="Оберіть гаманець", reply_markup=create_wallet_list_menu(telegram_id, "to_down")
    )


@dp.message_handler(Text(equals="Зробити перевод"))
async def to_transfer(message: Message):
    """"""

    telegram_id = message.from_user.id

    await message.answer(
        text="Оберіть гаманець", reply_markup=create_wallet_list_menu(telegram_id, "transfer")
    )


@dp.message_handler(Text(equals="Перевірити баланс"))
async def check_balance(message: Message):
    """"""

    telegram_id = message.from_user.id

    await message.answer(
        text="Оберіть гаманець", reply_markup=create_wallet_list_menu(telegram_id, "check")
    )


@dp.message_handler(Text(equals="Видалити гаманець"))
async def check_balance(message: Message):
    """Delete the wallet"""

    telegram_id = message.from_user.id

    await message.answer(
        text="Оберіть гаманець", reply_markup=create_wallet_list_menu(telegram_id, "delete")
    )


class FormToUp(StatesGroup):
    amount = State()


class FormToDown(StatesGroup):
    amount = State()


class FormToTransfer(StatesGroup):
    to_wallet_number = State()  # ID of the wallet to which the transfer is made
    amount = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('users_wallet_'))
async def process_callback_menu_currency(callback_query: CallbackQuery, state: FSMContext):
    call_data = callback_query.data
    wallet_number = call_data.split('_')[-1]

    if 'to_up' in call_data:
        await FormToUp.amount.set()
        await state.update_data(wallet_number=wallet_number)
        await callback_query.message.answer("Введіть суму для поповнення", reply_markup=cancel_menu)

    if 'to_down' in call_data:
        await FormToDown.amount.set()
        await state.update_data(wallet_number=wallet_number)
        await callback_query.message.answer("Введіть суму для списання", reply_markup=cancel_menu)

    if 'transfer' in call_data:
        await FormToTransfer.to_wallet_number.set()
        await state.update_data(wallet_number=wallet_number)
        await callback_query.message.answer("Введіть номер гаманця на який буде здійснений перевод:"
                                            , reply_markup=cancel_menu)

    if 'check' in call_data:
        wallet_data = get_wallet(wallet_number)
        wallet_title = wallet_data.get("Wallet", {}).get("title", "")
        wallet_description = wallet_data.get("Wallet", {}).get("description", "")
        wallet_amount = wallet_data.get("Wallet", {}).get("amount", 0)
        wallet_currency_id = wallet_data.get("Wallet", {}).get("basic_currency_id", 0)
        wallet_number = wallet_data.get("Wallet", {}).get("number", 0)
        currency_data = get_currency(wallet_currency_id)
        currency_symbol = currency_data.get("Currency", {}).get("symbol", "")
        await callback_query.message.answer(
            f"Назва: {wallet_title}\n"
            f"Опис: {wallet_description}\n"
            f"Номер: {wallet_number}\n"  
            f"Баланс: {wallet_amount} {currency_symbol}"
        )

    if 'delete' in call_data:
        wallet_data = get_wallet(wallet_number)
        wallet_title = wallet_data.get("Wallet", {}).get("title", "")
        delete_wallet(wallet_number)
        if delete_wallet:
            await callback_query.message.answer(
                f"Гаманець '{wallet_title}' був успішно видалений.",
                reply_markup=profile_menu
            )
        else:
            await callback_query.message.answer(
                f"Трапилася попилка при виконанні операції.",
                reply_markup=profile_menu
            )


@dp.message_handler(state=FormToUp.amount)
async def process_amount_to_up(message: Message, state: FSMContext):
    user_data = await state.get_data()
    wallet_number = user_data['wallet_number']

    try:
        amount = float(message.text)
        if amount > 0:
            wallet_data = to_up(wallet_number, amount)
            wallet_title = wallet_data.get("Wallet", {}).get("title", "Unknown")
            wallet_currency_id = wallet_data.get("Wallet", {}).get("basic_currency_id", 0)
            currency_data = get_currency(wallet_currency_id)
            currency_symbol = currency_data.get("Currency", {}).get("symbol", "")
            if wallet_title:
                await message.answer(f"Гаманець '{wallet_title}' був поповнений на {amount} {currency_symbol}.",
                                     reply_markup=profile_menu)
            else:
                await message.answer("Трапилася помилка при операції.")
            await state.finish()
        else:
            await message.answer("Сума має перевищувати 0. Введіть ще раз:")
    except ValueError:
        await message.answer("Введіть правильне число:")


@dp.message_handler(state=FormToDown.amount)
async def process_amount_to_down(message: Message, state: FSMContext):
    user_data = await state.get_data()
    wallet_number = user_data['wallet_number']

    try:
        amount = float(message.text)
        if amount > 0:
            wallet_data = to_down(wallet_number, amount)
            if wallet_data:
                wallet_title = wallet_data.get("Wallet", {}).get("title", "Unknown")
                wallet_currency_id = wallet_data.get("Wallet", {}).get("basic_currency_id", 0)
                currency_data = get_currency(wallet_currency_id)
                currency_symbol = currency_data.get("Currency", {}).get("symbol", "")
                await message.answer(f"З гаманця '{wallet_title}' було списано {amount} {currency_symbol}.",
                                     reply_markup=profile_menu)
                await state.finish()
            else:
                await message.answer("Недостатньо коштів на балансі. Введіть ще раз:")
        else:
            await message.answer("Сума має перевищувати 0. Введіть ще раз:")
    except ValueError:
        await message.answer("Введіть правильне число:")


@dp.message_handler(state=FormToTransfer.to_wallet_number)
async def process_wallet_number_to_transfer(message: Message, state: FSMContext):
    try:
        to_wallet_number = int(message.text)
        if len(str(to_wallet_number)) == 6:
            async with state.proxy() as data:
                data['to_wallet_number'] = str(message.text)
            wallet_data = get_wallet(to_wallet_number)
            if wallet_data:
                await message.answer("Введіть суму для переведення")
                await FormToTransfer.next()
            else:
                await message.answer("Введено неправильний номер гаманця. Спробуйте ще раз:")
        else:
            await message.answer("Введіть 6-ти значний номер:")
    except ValueError:
        await message.answer("Введіть правильний номер:")


@dp.message_handler(state=FormToTransfer.amount)
async def process_amount_to_transfer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    from_wallet_number = user_data['wallet_number']
    to_wallet_number = user_data['to_wallet_number']

    try:
        amount = float(message.text)
        if amount > 0:
            transfer_data = transfer(from_wallet_number, to_wallet_number, amount)
            if transfer_data:
                from_wallet_title = transfer_data.get("Transfer", {}).get("from_wallet_title", "Unknown")
                to_wallet_title = transfer_data.get("Transfer", {}).get("to_wallet_title", "Unknown")
                wallet_currency_id = transfer_data.get("Transfer", {}).get("basic_currency_id", 0)
                currency_data = get_currency(wallet_currency_id)
                currency_symbol = currency_data.get("Currency", {}).get("symbol", "")
                await message.answer(f"З гаманця '{from_wallet_title}' на '{to_wallet_title}' було переведено {amount} {currency_symbol}.",
                                     reply_markup=profile_menu)
                await state.finish()
            else:
                await message.answer("Недостатньо коштів на балансі. Введіть ще раз:")
        else:
            await message.answer("Сума має перевищувати 0. Введіть ще раз:")
    except ValueError:
        await message.answer("Введіть правильне число:")
