from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Все тикеты", callback_data="admin_all_tickets")],
            [InlineKeyboardButton(text="⏳ Открытые тикеты", callback_data="admin_open_tickets")],
            [InlineKeyboardButton(text="📢 Уведомление о новых", callback_data="admin_notify")]
        ]
    )