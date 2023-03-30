from aiogram import Dispatcher

from tgbot.handlers import admin
from tgbot.handlers import start
from tgbot.handlers import play


def register(dp: Dispatcher) -> None:
    admin.register(dp)
    start.register(dp)
    play.register(dp)
