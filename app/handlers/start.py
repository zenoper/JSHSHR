from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.keyboards import main, inline_cars
from app.states import Register

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Hi! you are in name state", reply_markup=await inline_cars())


@router.message(Command('help'))
async def help(message: Message):
    await message.answer("/help")


@router.message(F.text == 'ok', Register.number)
async def how(message: Message):
    await message.answer("Good")


@router.message(F.text)
async def how(message: Message):
    text = message.text
    await message.answer(text)