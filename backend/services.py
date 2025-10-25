from bson import ObjectId
from datetime import date, datetime
from database import expenses_collection
import traceback

# ------------------------
# Helper: Convert MongoDB document to dict
# ------------------------
def expense_helper(expense) -> dict:
    try:
        return {
            "id": str(expense["_id"]),
            "serialNo": expense.get("serialNo"),
            "title": expense.get("title"),
            "amount": expense.get("amount"),
            "category": expense.get("category"),
            "date": expense.get("date"),
        }
    except Exception as e:
        print("Error converting expense:", e)
        traceback.print_exc()
        return {}

# ------------------------
# Helper: Get next serial number for a given date
# ------------------------
async def get_next_serial_number_for_date(date_str: str) -> int:
    """
    Returns the next serial number for the given date.
    Serial numbers reset each day.
    """
    last_expense = await expenses_collection.find_one(
        {"date": date_str},
        sort=[("serialNo", -1)]
    )
    if last_expense and "serialNo" in last_expense:
        return last_expense["serialNo"] + 1
    return 1

# ------------------------
# CREATE: Add a new expense
# ------------------------
async def add_expense(expense_data: dict):
    try:
        print("\n--- [ADD EXPENSE DEBUG] ---")
        print("Incoming data:", expense_data)

        # Convert date object to string if necessary
        if isinstance(expense_data.get("date"), (date, datetime)):
            expense_data["date"] = expense_data["date"].isoformat()

        # If date not provided, set today
        if not expense_data.get("date"):
            expense_data["date"] = date.today().isoformat()

        # Assign serialNo for the date
        expense_data["serialNo"] = await get_next_serial_number_for_date(expense_data["date"])

        # Insert into MongoDB
        result = await expenses_collection.insert_one(expense_data)
        print("Inserted ID:", result.inserted_id)

        new_expense = await expenses_collection.find_one({"_id": result.inserted_id})
        if not new_expense:
            print("No expense found after insert!")
            return {"error": "Expense not found after insert"}

        print("Returning helper format:", expense_helper(new_expense))
        return expense_helper(new_expense)

    except Exception as e:
        print("Add Expense Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# ------------------------
# READ: List all expenses
# ------------------------
async def list_expenses():
    try:
        print("\n--- [LIST EXPENSES DEBUG] ---")
        expenses = []
        # Sort by date, then serialNo
        async for exp in expenses_collection.find().sort([("date", 1), ("serialNo", 1)]):
            expenses.append(expense_helper(exp))
        print("Total expenses fetched:", len(expenses))
        return expenses
    except Exception as e:
        print("List Expenses Error:", e)
        traceback.print_exc()
        return []

# ------------------------
# UPDATE: Update an existing expense
# ------------------------
async def update_expense(id: str, data: dict):
    try:
        print(f"\n--- [UPDATE EXPENSE DEBUG] --- ID: {id}")
        print("Update data:", data)

        expense = await expenses_collection.find_one({"_id": ObjectId(id)})
        if not expense:
            print("Expense not found!")
            return {"error": "Expense not found"}

        # Prevent accidental date change for now
        data.pop("date", None)

        await expenses_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated = await expenses_collection.find_one({"_id": ObjectId(id)})

        print("Updated expense:", updated)
        return expense_helper(updated)

    except Exception as e:
        print("Update Expense Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# ------------------------
# DELETE: Delete an expense
# ------------------------
async def delete_expense(id: str):
    try:
        print(f"\n--- [DELETE EXPENSE DEBUG] --- ID: {id}")

        result = await expenses_collection.delete_one({"_id": ObjectId(id)})
        print("Deleted count:", result.deleted_count)

        if result.deleted_count == 0:
            return {"message": "No expense found to delete"}
        return {"message": "Expense deleted successfully"}

    except Exception as e:
        print("Delete Expense Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# ------------------------
# TOTALS: Get totals by date
# ------------------------
async def get_totals_by_date(target_date: str = None):
    """
    Returns total expenses for a specific date, and totals per category.
    If no date provided, defaults to today.
    """
    from bson.son import SON

    if not target_date:
        target_date = date.today().isoformat()

    try:
        # Aggregate totals per category for the date
        pipeline = [
            {"$match": {"date": target_date}},
            {
                "$group": {
                    "_id": "$category",
                    "total_amount": {"$sum": "$amount"},
                    "count": {"$sum": 1}
                }
            }
        ]

        by_category = []
        cursor = expenses_collection.aggregate(pipeline)
        async for doc in cursor:
            by_category.append({
                "category": doc["_id"],
                "total_amount": doc["total_amount"],
                "count": doc["count"]
            })

        # Aggregate total amount for the date
        total_pipeline = [
            {"$match": {"date": target_date}},
            {"$group": {"_id": None, "total_amount": {"$sum": "$amount"}}}
        ]

        total_cursor = expenses_collection.aggregate(total_pipeline)
        total = 0
        async for t in total_cursor:
            total = t["total_amount"]

        return {"date": target_date, "total_amount": total, "by_category": by_category}

    except Exception as e:
        print("Get Totals Error:", e)
        traceback.print_exc()
        return {"error": str(e)}







# *********************************************************************************************************


# services.py
# from bson import ObjectId
# from database import expenses_collection
# from models import Expense

# # Helper function to convert MongoDB document to dict
# def expense_helper(expense) -> dict:
#     return {
#         "id": str(expense["_id"]),
#         "title": expense["title"],
#         "amount": expense["amount"],
#         "category": expense["category"],
#         "date": expense["date"],
#     }


# async def add_expense(expense_data: dict):
#     expense = await expenses_collection.insert_one(expense_data)
#     new_expense = await expenses_collection.find_one({"_id": expense.inserted_id})
#     return expense_helper(new_expense)


# async def list_expenses():
#     expenses = []
#     async for expense in expenses_collection.find():
#         expenses.append(expense_helper(expense))
#     return expenses


# async def update_expense(id: str, data: dict):
#     expense = await expenses_collection.find_one({"_id": ObjectId(id)})
#     if expense:
#         await expenses_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         updated = await expenses_collection.find_one({"_id": ObjectId(id)})
#         return expense_helper(updated)
#     return False


# async def delete_expense(id: str):
#     result = await expenses_collection.delete_one({"_id": ObjectId(id)})
#     return result.deleted_count > 0




# *****************************************************************************************


# Data Access Layer
# services.py
# from database import expense_collection
# from models import Expense
# from bson import ObjectId

# def expense_helper(expense) -> dict:
#     return {
#         "id": str(expense["_id"]),
#         "title": expense["title"],
#         "amount": expense["amount"],
#         "category": expense["category"],
#         "date": expense["date"],
#     }

# # CREATE
# async def add_expense(expense_data: dict):
#     expense = await expense_collection.insert_one(expense_data)
#     new_expense = await expense_collection.find_one({"_id": expense.inserted_id})
#     return expense_helper(new_expense)

# # READ (ALL)
# async def list_expenses():
#     expenses = []
#     async for expense in expense_collection.find():
#         expenses.append(expense_helper(expense))
#     return expenses

# # UPDATE
# async def update_expense(id: str, data: dict):
#     expense = await expense_collection.find_one({"_id": ObjectId(id)})
#     if expense:
#         await expense_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         updated = await expense_collection.find_one({"_id": ObjectId(id)})
#         return expense_helper(updated)
#     return False

# # DELETE
# async def delete_expense(id: str):
#     result = await expense_collection.delete_one({"_id": ObjectId(id)})
#     return result.deleted_count > 0
