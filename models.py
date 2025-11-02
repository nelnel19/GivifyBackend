from flask_bcrypt import Bcrypt
from database import users_collection

bcrypt = Bcrypt()

class UserModel:
    @staticmethod
    def create_user(name, email, password, age, role="user"):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = {
            "name": name,
            "email": email.lower(),
            "password": hashed_password,
            "age": int(age),
            "role": role,
            "disabled": False
        }
        users_collection.insert_one(user)
        return user

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email.lower()})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.check_password_hash(stored_password, provided_password)