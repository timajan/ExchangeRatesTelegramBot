from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_main_menu(auth=False):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отримати список курс'),
                KeyboardButton(text='Авторизація' if not auth else 'Кабінет')
            ],
        ],
        resize_keyboard=True
    )
    return main_menu


def create_menu_keyboard(text, menu_text='Меню', request_contact=False):
    keyboard_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"{text}", request_contact=request_contact)
            ],
            [
                KeyboardButton(text=menu_text),
            ],
        ],

        resize_keyboard=True
    )
    return keyboard_menu


back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад до старту")
        ]
    ],
    resize_keyboard=True
)


cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Відміна")
        ]
    ],
    resize_keyboard=True
)
