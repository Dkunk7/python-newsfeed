from os import getenv
from click import echo
from flask import session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# When using sqlalchemy, you use python classes to make the models

# Note that the getenv() function is part of Python's built-in os module. But because we used a .env file to fake the environment variable,
# we need to first call load_dotenv() from the python-dotenv module. In production, DB_URL will be a proper environment variable.

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0) # manages overall connection to the db
Session = sessionmaker(bind=engine) # generates temporary connections for performing create, read, update, delete operations (CRUD)
Base = declarative_base() # helps map the models to real MySQL tables