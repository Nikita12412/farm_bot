from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from sqlalchemy import Integer,Float,Text,String,DateTime,Boolean,select
from datetime import datetime,timedelta

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/farm"
engine = create_async_engine(DATABASE_URL)
session_local = async_sessionmaker(engine,expire_on_commit=True)

async def get_session():
    async with session_local() as session:
        yield session

class Base(DeclarativeBase):
    pass

class Storage(Base):
    __tablename__ = "storage"
    id:Mapped[int] = mapped_column(primary_key=True)
    player_id:Mapped[int] = mapped_column(Integer)
    plant_name:Mapped[str] = mapped_column(String)
    amount:Mapped[float] = mapped_column(Float)

class Plant(Base):
    __tablename__ = "plants"
    id:Mapped[int] = mapped_column(primary_key=True)
    player_id:Mapped[int] = mapped_column(Integer)
    planting_datetime:Mapped[datetime] = mapped_column(DateTime)
    is_grown:Mapped[bool] = mapped_column(Boolean)
    harvest:Mapped[float] = mapped_column(Float)
    plant_name:Mapped[str] = mapped_column(String)

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    telegram_id:Mapped[int] = mapped_column(Integer,unique=True)
    balance:Mapped[float] = mapped_column(Float)

async def add_user(telegram_id):
    async with session_local() as session:
        try:
            user = User(telegram_id = telegram_id,balance = 0)
            session.add(user)
            await session.commit()
            return True
        except:
            return False

async def add_plant(telegram_id,harvest,grows_time,plant_name):
    async with session_local() as session:
        plant = Plant(player_id = telegram_id,planting_datetime = datetime.now() + timedelta(hours = grows_time),is_grown = False,harvest = harvest,plant_name = plant_name)
        session.add(plant)
        await session.commit()

async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def get_plants():
    async with session_local() as session:
        query = select(Plant)
        plants:list[Plant] = (await session.execute(query)).scalars().all()
        return plants

async def mark_plant_as_grown(plant:Plant):
    async with session_local() as session:
        plant = await session.get(Plant,plant.id)
        plant.is_grown = True
        await session.commit()

async def get_grown_plants_by_player(telegram_id):
    async with session_local() as session:
        query = select(Plant).where(Plant.player_id == telegram_id,Plant.is_grown == True)
        plants:list[Plant] = (await session.execute(query)).scalars().all()
        return plants
    
async def delete_plants(plants_ids:list[int]):
    async with session_local() as session:
        for plant_id in plants_ids:
            plant = await session.get(Plant,plant_id)
            await session.delete(plant)
        await session.commit()

async def harvest_crop(telegram_id):
    plants = await get_grown_plants_by_player(telegram_id)
    plants_ids = []
    harvested_plants = {}
    for plant in plants:
        if not plant.plant_name in harvested_plants:
            harvested_plants[plant.plant_name] = 0
        harvested_plants[plant.plant_name] += plant.harvest
        plants_ids.append(plant.id)
    await delete_plants(plants_ids)
    for plant_name,amount in harvested_plants.items():
        await add_harvested_plant(telegram_id,plant_name,amount)
    return harvested_plants

async def add_harvested_plant(telegram_id,plant_name,amount):
    async with session_local() as session:
        storage_query = select(Storage).where(Storage.player_id == telegram_id,Storage.plant_name == plant_name)
        storage_item = (await session.execute(storage_query)).scalar_one_or_none()
        if storage_item:
            storage_item.amount += amount
        else:
            storage_item = Storage(player_id = telegram_id,plant_name = plant_name,amount = amount)
            session.add(storage_item)
        await session.commit()