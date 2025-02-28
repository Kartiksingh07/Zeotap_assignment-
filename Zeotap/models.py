from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import metadata, Base  # Correct import from database.py

# Define tables using SQLAlchemy
sheets = Table(
    "sheets",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
)

cells = Table(
    "cells",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("sheet_id", Integer, ForeignKey("sheets.id")),
    Column("row", Integer),
    Column("col", Integer),
    Column("value", String),
)

# Pydantic models (for validation and request bodies)
class Spreadsheet(BaseModel):
    name: str
    cells: list  # List of CellData objects

class CellData(BaseModel):
    row: int
    col: int
    value: str
