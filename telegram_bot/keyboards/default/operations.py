from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_users_wallets


operations_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поповнити '),
            KeyboardButton(text='Списати')
        ],
        [
            KeyboardButton(text='Зробити перевод'),
            KeyboardButton(text='Перевірити баланс')
        ],
        [
            KeyboardButton(text='Видалити гаманець'),
            KeyboardButton(text='Назад до кабінету'),
        ],
    ],
    resize_keyboard=True
)
