import pyodbc
import os
from dotenv import load_dotenv

def getSQLConnection():
    load_dotenv()
    dbname = os.environ.get('DBNAME')
    dbServer = os.environ.get('SERVER')
    cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=' + dbServer + ';'
                      'Database=' + dbname + ';'
                      'Trusted_Connection=yes;')
    return cnxn