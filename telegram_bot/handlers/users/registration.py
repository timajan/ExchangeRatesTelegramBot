from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import get_user, create_user
from main import dp
from keyboards.default.main_menu import create_menu_keyboard, create_main_menu


# States
class Form(StatesGroup):
    phone = State()
    full_name = State()


@dp.message_handler(Text(equals=['Авторизація']), state='*')
async def show_menu(message: Message, state: FSMContext):
    """Start a form"""

    telegram_id = message.from_user.id
    user, status = get_user(telegram_id)
    if status == 200:
        await message.answer('Ви вже авторизовані.', reply_markup=create_main_menu(auth=True))
    else:
        await Form.phone.set()

        await message.answer("Прохання поділитися своїм номером телефона, 👇натиснувши відповідну кнопку меню.",
                             reply_markup=create_menu_keyboard(
                                 text="Поділитися своїм номером телефону",
                                 request_contact=True,
                                 menu_text='Відміна',
                             ))


@dp.message_handler(content_types=ContentType.CONTACT, state=Form.phone)
async def get_phone(message: Message, state: FSMContext):
    """
    Process user phone
    """

    async with state.proxy() as data:
        data['phone_number'] = str(message.contact.phone_number).replace('+', '')

    await Form.next()
    await message.answer("Ваше ПІБ")


@dp.message_handler(state=Form.full_name)
async def process_full_name(message: Message, state: FSMContext):
    """
    Process user full_name
    """

    telegram_id = message.from_user.id
    username = message.from_user.username

    async with state.proxy() as data:
        data['full_name'] = message.text

    if len(data['full_name']) > 64:
        await message.answer("Занадто довге повідомлення. Введіть до 64 символів")
    else:
        user_data = {
            "name": data['full_name'],
            "phone": data['phone_number'],
            "username": username,
            "telegram_id": telegram_id,
        }

        response, status_code = create_user(user_data)
        if status_code == 201:
            await state.finish()
            await message.answer("Ви успішно зареєструвалися", reply_markup=create_main_menu(auth=True))
        else:
            await message.answer("Трапилася помилка. Спробуйте пізніше", reply_markup=create_main_menu(auth=False))
