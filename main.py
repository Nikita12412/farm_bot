from aiogram import Dispatcher,Bot,types
from aiogram import F
from aiogram.filters import Command,CommandObject
import asyncio

apitoken = '8557827638:AAG21pzqTqu6FCOiAYBRqi9Q8eDSbCraV1c'
bot = Bot(apitoken)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer("Привет")

asyncio.run(dp.start_polling(bot))