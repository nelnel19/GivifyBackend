from pymongo import MongoClient

# Replace with your MongoDB URI
MONGO_URI = "mongodb+srv://arnel123:arnel123@cluster0.tpjir.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# Create a database
db = client["givify_db"]

# Create a collection for users
users_collection = db["users"]
campaigns_collection = db["campaigns"]  # Collection name
donations_collection = db["donations"]