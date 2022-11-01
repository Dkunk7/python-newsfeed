from os import getenv
# from click import echo
# from flask import session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from flask import g

# When using sqlalchemy, you use python classes to make the models

# Note that the getenv() function is part of Python's built-in os module. But because we used a .env file to fake the environment variable,
# we need to first call load_dotenv() from the python-dotenv module. In production, DB_URL will be a proper environment variable.

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0) # manages overall connection to the db
Session = sessionmaker(bind=engine) # generates temporary connections for performing create, read, update, delete operations (CRUD)
Base = declarative_base() # helps map the models to real MySQL tables

def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)



# Whenever this function (get_db() below) is called, it returns a new session-connection object. Other modules in the app can import Session directly from the db package,
# but using a function means that we can perform additional logic before creating the database connection.

# For instance, if get_db() is called twice in the same route, we won't want to create a second connection. Rather, it will make more sense to return the existing connection.
# But how will we know if a connection has already been created per route?

# This is where the Flask application context helps. Flask creates a new context every time a server request is made. When the request ends, the context is removed from the app.
# These temporary contexts provide global variables, like the g object, that can be shared across modules as long as the context is still active.
# vvv
def get_db():
    if 'db' not in g:
        # store db connection in app context
        g.db = Session()
    return g.db

# The get_db() function now saves the current connection on the g object, if it's not already there.
# Then it returns the connection from the g object instead of creating a new Session instance each time.

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()