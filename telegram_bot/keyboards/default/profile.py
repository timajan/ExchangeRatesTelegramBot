from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

profile_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Переглянути гаманці"),
            KeyboardButton(text="Створити новий гаманець")
        ],
        [
            KeyboardButton(text="Вийти"),
            KeyboardButton(text="Назад до старту")
        ]
    ],
    resize_keyboard=True
)


back_to_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад до кабінету')
        ]
    ],
    resize_keyboard=True
)
