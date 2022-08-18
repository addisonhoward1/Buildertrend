from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def GetSQLAlchemy():
    load_dotenv()
    dbServer = os.environ.get('SERVER')
    dbName = os.environ.get('DBNAME')    
    engine = create_engine(
               f"mssql+pyodbc://{dbServer}/{dbName}?driver=SQL Server",
               echo=False)
    return engine