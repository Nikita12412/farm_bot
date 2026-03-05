from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,mapped_column
from sqlalchemy import Integer,Float,Text,String,DateTime,Boolean

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/farm"
engine = create_async_engine(DATABASE_URL,echo = True)
session_local = async_sessionmaker(engine,expire_on_commit=True)

async def get_session():
    async with session_local() as session:
        yield session

class Base(DeclarativeBase):
    pass

class Plants(Base):
    __tablename__ = "plants"
    id = mapped_column(primary_key=True)
    player_id = mapped_column(Integer)
    planting_datetime = mapped_column(DateTime)
    is_grown = mapped_column(Boolean)

async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)