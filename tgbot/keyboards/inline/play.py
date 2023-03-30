from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


callback_data = CallbackData("play")


def _make_callback_data() -> str:
    return callback_data.new()


def keyboard(user_attempts: int, total_attempts: int) -> InlineKeyboardMarkup:
    _keyboard = InlineKeyboardMarkup()

    _keyboard.add(InlineKeyboardButton(text=f"Проверить удачу 🍀 ({total_attempts - user_attempts}/{total_attempts})", callback_data=_make_callback_data()))

    return _keyboard
