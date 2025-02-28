from fastapi import APIRouter, HTTPException
from database import database
from models import sheets, cells, Spreadsheet, CellData

router = APIRouter()

# Create a New Spreadsheet
@router.post("/create_sheet/")
async def create_sheet(sheet: Spreadsheet):
    query = sheets.insert().values(name=sheet.name)
    sheet_id = await database.execute(query)
    
    for cell in sheet.cells:
        query = cells.insert().values(sheet_id=sheet_id, row=cell.row, col=cell.col, value=cell.value)
        await database.execute(query)
    
    return {"message": "Spreadsheet created successfully!"}

# Get a Spreadsheet
@router.get("/get_sheet/{sheet_name}")
async def get_sheet(sheet_name: str):
    query = sheets.select().where(sheets.c.name == sheet_name)
    sheet = await database.fetch_one(query)
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")
    
    query = cells.select().where(cells.c.sheet_id == sheet["id"])
    data = await database.fetch_all(query)
    
    return {"name": sheet_name, "cells": [{"row": r["row"], "col": r["col"], "value": r["value"]} for r in data]}

# Update a Cell
@router.put("/update_cell/{sheet_name}")
async def update_cell(sheet_name: str, cell: CellData):
    query = sheets.select().where(sheets.c.name == sheet_name)
    sheet = await database.fetch_one(query)
    if not sheet:
        raise HTTPException(status_code=404, detail="Spreadsheet not found")

    query = cells.update().where(
        (cells.c.sheet_id == sheet["id"]) &
        (cells.c.row == cell.row) &
        (cells.c.col == cell.col)
    ).values(value=cell.value)

    await database.execute(query)
    return {"message": "Cell updated successfully!"}
