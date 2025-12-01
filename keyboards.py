# keyboards.py

from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def generate_options_keyboard(options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in options:
        callback_data = "right_answer" if option == right_answer else "wrong_answer"
        builder.add(InlineKeyboardButton(text=option, callback_data=callback_data))
    builder.adjust(1)
    return builder.as_markup()

def get_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)