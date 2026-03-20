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

class Plant(Base):
    __tablename__ = "plants"
    id:Mapped[int] = mapped_column(primary_key=True)
    player_id:Mapped[int] = mapped_column(Integer)
    planting_datetime:Mapped[datetime] = mapped_column(DateTime)
    is_grown:Mapped[bool] = mapped_column(Boolean)
    harvest:Mapped[float] = mapped_column(Float)

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

async def add_plant(telegram_id,harvest,grows_time):
    async with session_local() as session:
        plant = Plant(player_id = telegram_id,planting_datetime = datetime.now() + timedelta(minutes = grows_time),is_grown = False,harvest = harvest)
        session.add(plant)
        await session.commit()

async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def get_plants():
    async with session_local() as session:
        query = select(Plant)
        plants:list[Plant] = (await session.execute(query)).all()
        return plants

async def mark_plant_as_grown(plant:Plant):
    async with session_local() as session:
        plant.is_grown = True
        await session.commit()