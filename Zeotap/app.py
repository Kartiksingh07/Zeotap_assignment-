from fastapi import FastAPI
from contextlib import asynccontextmanager
import databases
import sqlalchemy

DATABASE_URL = "postgresql://postgres:Kartik_S%401@localhost:5432/spreadsheet_db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
