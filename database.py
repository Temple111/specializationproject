import sqlite3 # this is bcos we used sqlite3 to create the backend database
from flask import g # "g" is a global variable used for database connection
import os

def connect_to_database():
    # Get the absolute path to the current directory
    current_directory = os.path.abspath(os.path.dirname(__file__))

    # Join the current directory with the relative path to app.db
    db_path = os.path.join(current_directory, "app.db")

    # Connect to the database using the joined path
    sql = sqlite3.connect(db_path)
    sql.row_factory = sqlite3.Row
    return sql

def getDatabase():
    if not hasattr(g, "quizapp_db"): # this checks if g does not have an attribute called quizapp_db
         # creating the attribute if it does not exist
         g.quizapp_db = connect_to_database() # connecting it to the database gotten above to access the database 
    return g.quizapp_db # returning the stored database
