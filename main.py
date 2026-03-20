from aiogram import Dispatcher,Bot,types
from aiogram import F
from aiogram.filters import Command,CommandObject
from aiogram.filters.callback_data import CallbackData
import asyncio
from database import engine,create_tables,add_plant,add_user
from plantsmodels import PlantTemplate,plants_info
from growservice import grow_procces

apitoken = '8557827638:AAG21pzqTqu6FCOiAYBRqi9Q8eDSbCraV1c'
bot = Bot(apitoken)
dp = Dispatcher()


class PlantaPlantCalback(CallbackData,prefix = "plant"):
    telegram_id:int
    plant:str

@dp.callback_query(PlantaPlantCalback.filter())
async def proces_plant(callback:types.CallbackQuery,callback_data:PlantaPlantCalback):
    harvest = plants_info[callback_data.plant].base_yield
    grows_time = plants_info[callback_data.plant].growth_time
    await add_plant(callback.from_user.id,harvest,grows_time)
    await callback.message.answer(f"вы посадили {callback_data.plant}")

@dp.message(Command('start'))
async def start(message:types.Message):
    if await add_user(telegram_id= message.from_user.id):
        await message.answer("Приветствую вас, хозяин фермы! 🏡\nВы попали в симулятор фермерской жизни. У вас есть участок земли, стартовый капитал и море возможностей.\nЧто доступно:\n🔸 посадка культур и сбор урожая;\n🔸 улучшение фермы;\n🔸 торговля на рынке.\nИспользуйте меню ниже, чтобы начать своё приключение!")
    else:
        await message.answer("Снова приветствую вас, хозяин фермы! 🏡\nВы попали в симулятор фермерской жизни. У вас есть участок земли, стартовый капитал и море возможностей.\nЧто доступно:\n🔸 посадка культур и сбор урожая;\n🔸 улучшение фермы;\n🔸 торговля на рынке.\nИспользуйте меню ниже, чтобы начать своё приключение!")

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

#МЕНЮ ФЕРМЫ
@dp.callback_query(F.data == "open_farm_menu")
async def open_farm_menu(callback:types.CallbackQuery):
    farm_info = "информация о ферме"
    harvestbutton = types.InlineKeyboardButton(text = "Собрать урожай",callback_data = "crop_harvest")
    exportcropsbutton = types.InlineKeyboardButton(text = "Вывезти урожай",callback_data = "...")
    planplantsbutton = types.InlineKeyboardButton(text = "Посадить семена",callback_data = "plant_seeds")
    buynewfarmbuton = types.InlineKeyboardButton(text = "Купить новую ферму",callback_data = "...")
    row1 = [harvestbutton,exportcropsbutton]
    row2 = [planplantsbutton,buynewfarmbuton]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[row1,row2])
    await callback.message.answer(farm_info,reply_markup = keyboard)

@dp.callback_query(F.data == "crop_harvest")
async def crop_harvest(callback:types.CallbackQuery):
    await callback.message.answer("Вы собрали урожай")

@dp.callback_query(F.data == "plant_seeds")
async def plant_seeds(callback:types.CallbackQuery):
    seeds = {
        "помидоры":0,
        "яблоко":2,
        "тыквы":1
    }
    keyboard_rows = []
    for seedname,seedabmount in seeds.items():
        if seedabmount > 0:
            button = types.InlineKeyboardButton(text=f"{seedname}:{seedabmount}",callback_data=PlantaPlantCalback(telegram_id = callback.from_user.id,plant = seedname).pack())
            keyboard_rows.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await callback.message.answer("Вы можете посадить:",reply_markup=keyboard)

@dp.callback_query(F.data == "open_avtopark_menu")
async def open_avtopark_menu(callback:types.CallbackQuery):
    avtopark_info = "информация о автопарке"
    selectioncarbutton = types.InlineKeyboardButton(text = "Выбрать авто",callback_data = "...")
    sellcarbutton = types.InlineKeyboardButton(text = "Продать авто",callback_data = "...")
    buycarbutton = types.InlineKeyboardButton(text = "Купить авто",callback_data = "...")
    row1 = [selectioncarbutton]
    row2 = [sellcarbutton,buycarbutton]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[row1,row2])
    await callback.message.answer(avtopark_info,reply_markup = keyboard)

@dp.callback_query(F.data == "open_shop_menu")
async def open_shop_menu(callback:types.CallbackQuery):
    shop_info = "ассортимент магазина"
    buycarbutton = types.InlineKeyboardButton(text = "Продать авто",callback_data = "...")
    buyseedsbutton = types.InlineKeyboardButton(text = "Купить семена",callback_data = "...")
    buynewfarmbuton = types.InlineKeyboardButton(text = "Купить новую ферму",callback_data = "...")
    row1 = [buycarbutton]
    row2 = [buyseedsbutton]
    row3 = [buynewfarmbuton]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[row1,row2,row3])
    await callback.message.answer(shop_info,reply_markup = keyboard)

@dp.callback_query(F.data == "open_market_menu")
async def open_market_menu(callback:types.CallbackQuery):
    market_info = "цена продажи урожая"
    sellharvest = types.InlineKeyboardButton(text = "Продать урожай",callback_data = "sell_harvest")
    row = [sellharvest]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[row])
    await callback.message.answer(market_info,reply_markup = keyboard)

@dp.callback_query(F.data == "sell_harvest")
async def sell_harvest(callback:types.CallbackQuery):
    await callback.message.answer("Вы продали урожай")

async def main():
    await create_tables()
    grow_task = asyncio.create_task(grow_procces())
    await dp.start_polling(bot)

asyncio.run(main()) 