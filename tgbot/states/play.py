from aiogram.dispatcher.filters.state import State, StatesGroup


class PlayState(StatesGroup):
    playing = State()
