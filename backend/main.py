from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from models import Expense, ExpenseUpdate
from services import add_expense, list_expenses, update_expense, delete_expense, get_totals_by_date

app = FastAPI(title="Expense Tracker API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# CREATE: Add a new expense
# ------------------------
@app.post("/expenses")
async def create_expense(expense: Expense):
    expense_dict = expense.dict()
    result = await add_expense(expense_dict)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ------------------------
# READ: List all expenses
# ------------------------
@app.get("/expenses")
async def get_expenses():
    expenses = await list_expenses()
    return expenses

# ------------------------
# READ: Get totals by date
# ------------------------
@app.get("/expenses/totals")
async def get_expense_totals(date: str = Query(None, description="Date in YYYY-MM-DD format")):
    totals = await get_totals_by_date(date)
    if "error" in totals:
        raise HTTPException(status_code=400, detail=totals["error"])
    return totals

# ------------------------
# UPDATE: Update an existing expense
# ------------------------
@app.put("/expenses/{expense_id}")
async def update_expense_endpoint(expense_id: str, expense: ExpenseUpdate):
    update_data = expense.dict(exclude_unset=True)
    result = await update_expense(expense_id, update_data)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ------------------------
# DELETE: Delete an expense
# ------------------------
@app.delete("/expenses/{expense_id}")
async def delete_expense_endpoint(expense_id: str):
    result = await delete_expense(expense_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result




# ************************************************************************************************

# main.py
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# from models import Expense, ExpenseUpdate
# from database import expense_collection
# from services import add_expense, list_expenses, update_expense, delete_expense

# app = FastAPI(title = "Expense Tracker API")

# # Allow React frontend to call FastAPI
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Expense Tracker API running"}

# @app.post("/addExpenses")
# async def create_expense(expense: Expense):
#     new_expense = await add_expense(expense.dict())
#     return new_expense

# @app.get("/viewExpenses")
# async def get_expenses():
#     return await list_expenses()

# @app.put("/editExpenses/{id}")
# async def edit_expense(id: str, expense: ExpenseUpdate):
#     updated = await update_expense(id, expense.dict(exclude_unset=True))
#     if not updated:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return updated

# @app.delete("/deleteExpenses/{id}")
# async def remove_expense(id: str):
#     deleted = await delete_expense(id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return {"message": "Expense deleted successfully"}

# *********************************************************************************************

# from fastapi import FastAPI
# import logging

# logging.basicConfig(
#     level = logging.DEBUG,
#     format = "%(asctime)s - %(levelname)s - %(message)s"
# )

# app = FastAPI()

# @app.get("/")
# def read_root():
#     logging.debug("Hi Murali!")
#     return {"message": "Python is running perfectly inside venv!"}

