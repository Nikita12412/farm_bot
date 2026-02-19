from aiogram import Dispatcher,Bot,types
from aiogram import F
from aiogram.filters import Command,CommandObject
import asyncio

apitoken = '8557827638:AAG21pzqTqu6FCOiAYBRqi9Q8eDSbCraV1c'
bot = Bot(apitoken)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer("Приветствую вас, хозяин фермы! 🏡\nВы попали в симулятор фермерской жизни. У вас есть участок земли, стартовый капитал и море возможностей.\nЧто доступно:\n🔸 посадка культур и сбор урожая;\n🔸 улучшение фермы;\n🔸 торговля на рынке.\nИспользуйте меню ниже, чтобы начать своё приключение!")

asyncio.run(dp.start_polling(bot))