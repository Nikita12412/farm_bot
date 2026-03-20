import asyncio
from database import get_plants,mark_plant_as_grown
from datetime import datetime,timedelta
from plantsmodels import plants_info
import time

async def grow_procces():
    while True:
        await asyncio.sleep(3600)
        plants = await get_plants()
        current_time = datetime.now()
        print(plants)
        print("растения обновлены")
        for plant in plants:
            print(plant.planting_datetime,current_time)
            print("проходимся по растениям")
            if plant.planting_datetime <= current_time:
                print("Растение выросло")
                await mark_plant_as_grown(plant)