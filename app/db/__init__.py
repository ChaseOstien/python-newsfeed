from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
print("Before database connection code")
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()
print("After database connection code")

# This function initializes the database connection and also closes the database connection
def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)

# This function gets the database connection
def get_db():
    if 'db' not in g:
        # store db connection in app context
        g.db = Session()

    return Session()

# This function closes the database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()