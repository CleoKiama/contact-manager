import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add any production-specific settings
    MONGO_URI = os.environ.get(
        "MONGODB_URI"
    )  # For production MongoDB (like MongoDB Atlas)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
