from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from loader import dp, bot
from app.keyboards.default import menu_kb

from .menu import _menu

from app.states.search_state import Search

@dp.message_handler(Text("💤"), state=Search.search)
@dp.message_handler(Command("cancel"), state="*")
async def _cancel_command(message: types.message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await _menu(message)