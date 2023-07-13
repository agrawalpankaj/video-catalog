from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.config import Config

# Read configuration from environment variables and/or ".env" files
config = Config(".env")
ENVIRONMENT = config("ENVIRONMENT")
POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_PORT = config("POSTGRES_PORT")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASS = config("POSTGRES_PASS")
POSTGRES_DB = config("POSTGRES_DB")
DB_TYPE = config("DB_TYPE")

# Build the connection URL for the database
SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Uncomment the following lines and modify them to define and use other databases

"""

SQLite example:
from sqlalchemy.dialects import sqlite
DB_TYPE = "sqlite"
SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}:///path/to/database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

"""

"""

MongoDB example (using PyMongo):
from pymongo import MongoClient
DB_TYPE = "mongodb"
MONGO_HOST = config("MONGO_HOST")
MONGO_PORT = config("MONGO_PORT")
MONGO_USER = config("MONGO_USER")
MONGO_PASS = config("MONGO_PASS")
MONGO_DB = config("MONGO_DB")
MONGO_CONNECTION_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
client = MongoClient(MONGO_CONNECTION_URL)
database = client[MONGO_DB]
engine = create_engine('mongodb+pyodbc://', creator=lambda: database)

"""

# Additional databases can be defined similarly, based on the database you want to use.


# Create the database engine
engine = create_engine(f"{SQLALCHEMY_DATABASE_URL}")

# Create a session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


def get_db():
    """
    Obtain a database session.

    Returns:
        Session: A SQLAlchemy database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
