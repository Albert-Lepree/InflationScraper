import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file) # creates dbfile in memory. Can also use db_file inside ()
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def addToDB(nameOfColumn, db_file):
    pass

def addToDB(nameOfColumn, db_file, data):
    pass

def printAllData(db_file):
    pass
