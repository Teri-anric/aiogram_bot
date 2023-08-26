from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router(name="commands-router")



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привіт"
    )


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Операція скасована!")
    await state.clear()
