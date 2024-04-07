from pymongo import MongoClient
import os

# Retrieve MongoDB connection details from environment variables
MONGODB_URI = os.environ.get("MONGODB_URI")

# Create MongoDB client using the retrieved URI
client = MongoClient(MONGODB_URI)

# Access your database and collection as needed
db = client.library_management
