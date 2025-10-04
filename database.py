import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://arnel123:arnel123@ac-xyz-shard-00-00.tpjir.mongodb.net:27017,ac-xyz-shard-00-01.tpjir.mongodb.net:27017,ac-xyz-shard-00-02.tpjir.mongodb.net:27017/?ssl=true&replicaSet=atlas-xyz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["givify_db"]

users_collection = db["users"]
campaigns_collection = db["campaigns"]
donations_collection = db["donations"]
