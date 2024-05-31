from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def currency_inline_menu():
    inline_menu = InlineKeyboardMarkup(row_width=10)
    inline_menu.add(InlineKeyboardButton('Американський Долар', callback_data=f'currency_USD'))
    inline_menu.add(InlineKeyboardButton('Гривня', callback_data=f'currency_UAH'))
    inline_menu.add(InlineKeyboardButton('Австралійський Долар', callback_data=f'currency_AUD'))
    inline_menu.add(InlineKeyboardButton('Канадський Долар', callback_data=f'currency_CAD'))
    inline_menu.add(InlineKeyboardButton('Чеська Крона', callback_data=f'currency_CZK'))
    inline_menu.add(InlineKeyboardButton('Датська Крона', callback_data=f'currency_DKK'))
    inline_menu.add(InlineKeyboardButton('Угорський Форинт', callback_data=f'currency_HUF'))
    inline_menu.add(InlineKeyboardButton('Ізраїльський Шекель', callback_data=f'currency_ILS'))
    inline_menu.add(InlineKeyboardButton('Японська Єна', callback_data=f'currency_JPY'))
    inline_menu.add(InlineKeyboardButton('Латвійський Лат', callback_data=f'currency_LVL'))
    inline_menu.add(InlineKeyboardButton('Литовський Літ', callback_data=f'currency_LTL'))
    inline_menu.add(InlineKeyboardButton('Норвезька Крона', callback_data=f'currency_NOK'))
    inline_menu.add(InlineKeyboardButton('Словацька Крона', callback_data=f'currency_SKK'))
    inline_menu.add(InlineKeyboardButton('Шведська Крона', callback_data=f'currency_SEK'))
    inline_menu.add(InlineKeyboardButton('Швейцарський Франк', callback_data=f'currency_CHF'))
    inline_menu.add(InlineKeyboardButton('Британський Фунт', callback_data=f'currency_GBP'))
    inline_menu.add(InlineKeyboardButton('Білоруський Рубль', callback_data=f'currency_BYR'))
    inline_menu.add(InlineKeyboardButton('Євро', callback_data=f'currency_EUR'))
    inline_menu.add(InlineKeyboardButton('Грузинський Ларі', callback_data=f'currency_GEL'))
    inline_menu.add(InlineKeyboardButton('Польський Злотий', callback_data=f'currency_PLZ'))
    return inline_menu
