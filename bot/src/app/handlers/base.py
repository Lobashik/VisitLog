from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppData

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть веб-приложение",
            web_app={"url": "https://styleru.org/"}
        )]
    ])
    await message.answer("Добро пожаловать!", reply_markup=keyboard)