import asyncio
import random
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.utils.exceptions import MessageNotModified
from tgbot.config import Config

from tgbot.keyboards.inline import play
from tgbot.models.db import db
from tgbot.models.user_tg import UserTG
from tgbot.services.broadcasting import send_to_admins
from tgbot.states.play import PlayState


async def _start_lottery(call: types.CallbackQuery, user: UserTG, state: FSMContext, config: Config) -> None:
    if user.attempts >= config.misc.total_attempts:
        await user.delete_message(call.message.message_id)
        return

    await PlayState.playing.set()

    total_winners = await db.select([db.func.count()]).where(UserTG.has_won == True).gino.scalar()
    has_won = random.randint(1, 100) <= config.misc.win_chance * 100 and total_winners < config.misc.max_winners
    if has_won:
        await user.update(has_won=True).apply()
        text = f"""
{hlink('Пользователь', f'tg://user?id={user.id}')} выиграл
@{user.username} {user.first_name} {user.last_name}
"""
        await send_to_admins(call.bot, text)

    for _ in range(config.misc.spins_count - 1):
        await _randomize_message(call, user, config)
        await asyncio.sleep(config.misc.time_between_spins)
    await _stop_lottery(call, user, config, has_won)

    await user.update(attempts=user.attempts + 1).apply()

    if has_won:
        text = f"""
Поздравляю с победой{f', {user.info}' if user.info else ''}!

Ты выбил(а) свой заветный сет коктейлей🍷Надеемся, тебе было весело, и ты смог(ла) погрузиться атмосферу азарта.
Тебе скоро напишут, чтобы вручить приз 🤗
"""
        await user.send_message(text)
        await asyncio.sleep(0.5)
        await user.send_sticker(config.misc.happy_sticker)
    elif user.attempts >= config.misc.total_attempts:
        await user.send_sticker(config.misc.sad_sticker)
        await asyncio.sleep(0.5)
        text = """
К сожалению, попытки закончились ☹️
Не расстраивайся, солнце! Видимо, удача встала не стой ноги сегодня 🤷‍♂️

Зато это значит, что если не повезло в игре, повезет в любви 💝

Держи котика для хорошего настроения 😺
"""
        await user.send_message(text)
        await asyncio.sleep(0.5)
        await user.send_sticker(config.misc.sad_sticker2)
    else:
        await user.send_message("Упс! Попробуй еще раз",
                                reply_markup=play.keyboard(user_attempts=user.attempts,
                                                           total_attempts=config.misc.total_attempts))

    await state.finish()


async def _randomize_message(call: types.CallbackQuery, user: UserTG, config: Config) -> None:
    row = ""
    for _ in range(config.misc.row_length):
        row += random.choice(config.misc.icons)

    try:
        await user.edit_message_text(row, message_id=call.message.message_id)
    except MessageNotModified:
        pass


async def _stop_lottery(call: types.CallbackQuery, user: UserTG, config: Config, has_won: bool) -> None:
    row = ""
    if has_won:
        row = random.choice(config.misc.icons) * config.misc.row_length
    else:
        while True:
            row = ""
            for _ in range(config.misc.row_length):
                row += random.choice(config.misc.icons)

            if row.count(row[0]) != config.misc.row_length:
                break

    try:
        await user.edit_message_text(row, message_id=call.message.message_id)
    except MessageNotModified:
        pass


def register(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(_start_lottery,
                                       play.callback_data.filter())
