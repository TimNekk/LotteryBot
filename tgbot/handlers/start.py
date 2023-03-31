from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.message import ContentType

from tgbot.models.user_tg import UserTG
from tgbot.keyboards.inline import play
from tgbot.config import Config


async def start(message: types.Message, user: UserTG, config: Config) -> None:
    if user.attempts >= config.misc.total_attempts or user.has_won:
        return

    text = f"""
Добро пожаловать в <b>Барное казино</b>{f', {user.info}' if user.info else ''}.

Здесь у тебя есть возможность выиграть классные призы.
Настраивай свою удачу и Let's go играть! 🤞
"""

    await user.send_message(text,
                            reply_markup=play.keyboard(user_attempts=user.attempts,
                                                       total_attempts=config.misc.total_attempts))


async def sticker(message: types.Message, user: UserTG, config: Config) -> None:
    await user.send_message(message.sticker.file_id)


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(sticker,
                                content_types=[ContentType.STICKER])
