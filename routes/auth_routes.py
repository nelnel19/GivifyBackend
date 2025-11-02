from flask import Blueprint, request, jsonify
from models import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from database import users_collection

auth_routes = Blueprint("auth_routes", __name__)

# Register Route
@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    age = data.get("age")

    if not name or not email or not password or age is None:
        return jsonify({"error": "All fields are required"}), 400

    if int(age) < 18:
        return jsonify({"error": "You must be at least 18 years old to register"}), 400

    if UserModel.find_by_email(email):
        return jsonify({"error": "Email already registered"}), 400

    user = UserModel.create_user(name, email, password, age)
    return jsonify({"message": "User registered successfully"}), 201


# Login Route
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = UserModel.find_by_email(email)
    if not user or not UserModel.verify_password(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    if user.get("disabled", False):
        return jsonify({"error": "Account is disabled. Contact admin."}), 403

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "age": user["age"],
            "role": user.get("role", "user")  # ✅ Added role field
        }
    }), 200


# Get all users
@auth_routes.route("/users", methods=["GET"])
def get_users():
    users = []
    for user in users_collection.find():
        users.append({
            "_id": str(user["_id"]),
            "name": user.get("name", "N/A"),
            "email": user.get("email", "N/A"),
            "age": user.get("age", None),
            "role": user.get("role", "user"),  # ✅ Added role field
            "disabled": user.get("disabled", False)
        })
    return jsonify(users), 200


# Update user
@auth_routes.route("/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.json
    update_fields = {}

    if "name" in data:
        update_fields["name"] = data["name"]
    if "email" in data:
        update_fields["email"] = data["email"]
    if "age" in data:
        update_fields["age"] = int(data["age"])
    if "role" in data:  # ✅ Added role update
        update_fields["role"] = data["role"]

    users_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    user = users_collection.find_one({"_id": ObjectId(id)})

    return jsonify({
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"],
        "role": user.get("role", "user"),  # ✅ Added role field
        "disabled": user.get("disabled", False)
    }), 200


# Disable user
@auth_routes.route("/users/<id>/disable", methods=["PATCH"])
def disable_user(id):
    users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"disabled": True}})
    user = users_collection.find_one({"_id": ObjectId(id)})

    return jsonify({
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"],
        "role": user.get("role", "user"),  # ✅ Added role field
        "disabled": True
    }), 200

# Enable user
@auth_routes.route("/users/<id>/enable", methods=["PATCH"])
def enable_user(id):
    users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"disabled": False}})
    user = users_collection.find_one({"_id": ObjectId(id)})

    return jsonify({
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user.get("age", None),
        "role": user.get("role", "user"),  # ✅ Added role field
        "disabled": False
    }), 200