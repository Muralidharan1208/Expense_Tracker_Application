# database.py
# from motor.motor_asyncio import AsyncIOMotorClient

# MONGO_DETAILS = "mongodb://localhost:27017"
# client = AsyncIOMotorClient(MONGO_URI)

# database = client.expense_tracker   # database name
# expense_collection = database.get_collection("expenses") #collection name





# database.py
from motor.motor_asyncio import AsyncIOMotorClient

# Connection string for local MongoDB (Compass)
MONGO_URI = "mongodb://localhost:27017"

# Create client connection
client = AsyncIOMotorClient(MONGO_URI)

# Database and collection setup
database = client.expense_tracker          # database name
expenses_collection = database.get_collection("expenses")  # collection name


# *************************************************************************************


# database.py
# from motor.motor_asyncio import AsyncIOMotorClient
# import os

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# DB_NAME = os.getenv("expenses", "expense_tracker")

# client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
# db = client[DB_NAME]
