from db import get_users_wallets
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_wallet_list_menu(telegram_id, type_operations):
    wallets, status_code = get_users_wallets(telegram_id)
    inline_menu = InlineKeyboardMarkup(row_width=5)
    for wallet in wallets:
        inline_menu.add(InlineKeyboardButton(
            f'{wallet["title"]}',
            callback_data=f'users_wallet_{type_operations}_{wallet["number"]}'
        ))
    return inline_menu
