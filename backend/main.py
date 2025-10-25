from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from models import Expense, ExpenseUpdate
from database import expenses_collection  # ✅ corrected to match your database.py
from services import add_expense, list_expenses, update_expense, delete_expense

app = FastAPI(title="Expense Tracker API")

# ✅ Allow your frontend (React or any) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route to check if API is running
@app.get("/")
def home():
    return {"message": "Expense Tracker API running successfully 🚀"}


@app.post("/expenses")
async def create_expense(expense: Expense):
    new_expense = await add_expense(expense.dict())
    return new_expense


@app.get("/expenses")
async def get_expenses():
    return await list_expenses()


@app.put("/expenses/{id}")
async def edit_expense(id: str, expense: ExpenseUpdate):
    updated = await update_expense(id, expense.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated


@app.delete("/expenses/{id}")
async def remove_expense(id: str):
    deleted = await delete_expense(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}



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

