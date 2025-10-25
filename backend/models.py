# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

# Model for creating or returning an expense
class Expense(BaseModel):
    serialNo: Optional[int] = None  # auto-generated
    title: str
    amount: float
    category: str
    date: date

# Model for updating an expense (all fields optional)
class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    # date: Optional[date] = None




# **************************************************************


# models.py
# from pydantic import BaseModel
# from typing import Optional

# class Expense(BaseModel):
#     title: str
#     amount: float
#     category: str
#     date: str  # could also be datetime later

# class ExpenseUpdate(BaseModel):
#     title: Optional[str] = None
#     amount: Optional[float] = None
#     category: Optional[str] = None
#     date: Optional[str] = None
