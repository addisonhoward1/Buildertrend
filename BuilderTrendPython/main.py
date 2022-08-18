from pyexpat import ErrorString
from ClearTables import ClearingTables
from DataCleanser import DataCleansing
from EmailTemplate import ErrorEmail
from GetDriver import GettingDriver
from GetSQLEngine import GetSQLAlchemy
from GetScheduleInfo import GettingScheduleInfo
from GetSuperInfo import GettingSuperInfo
from LoginIn import LoggingIn

try:
    driver = GettingDriver()
    engine = GetSQLAlchemy()
    ClearingTables(engine)
    LoggingIn(driver)
    GettingSuperInfo(driver, engine)
    GettingScheduleInfo(driver, engine)
    DataCleansing(engine)

    print("End of Program")

except Exception as error:
    error_string=str(error)
    ErrorEmail(error_string)