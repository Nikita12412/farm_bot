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

@dp.message(Command("menu"))
async def menu(message:types.Message):
    farmbutton = types.InlineKeyboardButton(text = "Ферма",callback_data="open_farm_menu")
    avtoparkbutton = types.InlineKeyboardButton(text = "Автопарк",callback_data="open_avtopark_menu")
    shopbutton = types.InlineKeyboardButton(text = "Магазин",callback_data="open_shop_menu")
    marketbutton = types.InlineKeyboardButton(text = "Рынок",callback_data="open_market_menu")
    row1 = [farmbutton,avtoparkbutton]
    row2 = [shopbutton,marketbutton]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[row1,row2])
    await message.answer("меню",reply_markup=keyboard)

@dp.callback_query(F.data == "open_farm_menu")
async def open_farm_menu(callback:types.CallbackQuery):
    farm_info = "информация о ферме"
    harvestbutton = types.InlineKeyboardButton(text = "Собрать урожай",callback_data = "...")
    exportcropsbutton = types.InlineKeyboardButton(text = "Вывезти урожай",callback_data = "...")
    planplantsbutton = types.InlineKeyboardButton(text = "Посадить урожай",callback_data = "...")
    keybord = types.InlineKeyboardMarkup()

@dp.callback_query(F.data == "open_avtopark_menu")
async def open_avtopark_menu(callback:types.CallbackQuery):
    avtopark_info = "информация о автопарке"
    



asyncio.run(dp.start_polling(bot))