import databases
import sqlalchemy
from sqlalchemy.orm import declarative_base  # Correct import for SQLAlchemy 2.x

DATABASE_URL = "postgresql://postgres:Kartik_S%401@localhost:5432/spreadsheet_db"
database = databases.Database(DATABASE_URL)

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)  # Corrected
engine = sqlalchemy.create_engine(DATABASE_URL)
