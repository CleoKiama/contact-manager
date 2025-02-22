from flask_login import UserMixin
from bson.objectid import ObjectId  # Add this import
from app import login_manager, mongo
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
from flask import current_app


class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = str(user_data.get("_id"))  # Convert ObjectId to string
        self.email = user_data.get("email")
        self.password = user_data.get("password")

    @staticmethod
    def check_password(password_hash, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(password_hash, password)

    def get_id(self):
        return str(self.id)  # Override get_id to return string ID

    def get_reset_password_token(self, expires_in=600):
        # Create token that expires in 10 minutes (600 seconds)
        return jwt.encode(
            {"reset_password": str(self.id), "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
            user_data = mongo.db.users.find_one({"_id": ObjectId(id)})
            return User(user_data) if user_data else None
        except Exception as e:
            print(f"Token verification failed: {e}")  # Add logging
            return None


@login_manager.user_loader
def load_user(id):
    try:
        user_data = mongo.db.users.find_one(
            {"_id": ObjectId(id)}
        )  # Convert string ID back to ObjectId
        return User(user_data) if user_data else None
    except:
        return None
