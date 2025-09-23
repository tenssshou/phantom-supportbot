from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Создать тикет")],
            [KeyboardButton(text="❓ FAQ"), KeyboardButton(text="📊 История тикетов")]
        ],
        resize_keyboard=True
    )

def get_faq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Как создать тикет?", callback_data="faq_create")],
            [InlineKeyboardButton(text="Сколько ждать ответ?", callback_data="faq_time")],
            [InlineKeyboardButton(text="Как отменить тикет?", callback_data="faq_cancel")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ]
    )

def get_ticket_actions_keyboard(ticket_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Ответить", callback_data=f"answer_{ticket_id}")],
            [InlineKeyboardButton(text="🔒 Закрыть", callback_data=f"close_{ticket_id}")]
        ]
    )