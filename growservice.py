import asyncio
from database import get_plants
import datetime
from plantsmodels import plants_info

async def grow_procces():
    await asyncio.sleep(5)
    plants = await get_plants()
    for plant in plants:
        grows_time = plants_info[plant.]
        if plant.planting_datetime