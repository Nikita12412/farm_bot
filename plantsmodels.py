from dataclasses import dataclass
import datetime


@dataclass
class PlantTemplate:
    name:str
    base_yield:float
    growth_time:int
    price_per_kg:float
    seed_price:int

class PlantInstance:
    def __init__(self,template,player_id):
        self.template = template
        self.player_id = player_id
        self.planting_datetime = datetime.datetime.now()

plants_info = {
    "помидор":PlantTemplate("помидор",2,1,150,50),
    "яблоко":PlantTemplate("яблоко",3,2,300,140)
}