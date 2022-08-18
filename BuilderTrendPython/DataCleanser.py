import datetime
import pandas as pd
import re
from GetDBConnection import getSQLConnection

def DataCleansing(engine):

    cnxn = getSQLConnection()
    cursor = cnxn.cursor()
    
    df = pd.read_sql('select * from BTSuperRaw', engine) 
    rawData = df.values.tolist()   
    print(df.columns)
    for row in rawData:
        
        jobName = row[1]
        strtadds = row[2]
        city = row[3]
        usState = row[4]
        zipCode = row[5]
        projMngr = row[6]
        owner = row[7]
        phone = row[8]
        email = row[18]
        lotNumber = row[19]  
        
            
        cursor.execute('IF NOT EXISTS(select * from BuilderTrendScrape where Lot = ?) Begin insert into BuilderTrendScrape(Lot) values(?) End', lotNumber, lotNumber) 
        cursor.execute('update BuilderTrendScrape set [Job Name] = ? where Lot = ?', jobName, lotNumber)
        cursor.execute('update BuilderTrendScrape set [Street Address] = ? where Lot = ?', strtadds, lotNumber)
        cursor.execute('update BuilderTrendScrape set City = ? where Lot = ?', city, lotNumber)
        cursor.execute('update BuilderTrendScrape set State = ? where Lot = ?', usState, lotNumber)
        cursor.execute('update BuilderTrendScrape set ZIP = ? where Lot = ?', zipCode, lotNumber)
        cursor.execute('update BuilderTrendScrape set [Project Manager] = ? where Lot = ?', projMngr, lotNumber)
        cursor.execute('update BuilderTrendScrape set Owner = ? where Lot = ?', owner, lotNumber)
        cursor.execute('update BuilderTrendScrape set Phone = ? where Lot = ?', phone, lotNumber) 
        cursor.execute('update BuilderTrendScrape set Email = ? where Lot = ?', email, lotNumber)        
        cursor.commit() 
         
    df = pd.read_sql("select [Lot Number], Title, [Start], [End] from BTScheduleRaw where Title like 'Orientation'", engine)
    rawData = df.values.tolist()
    for row in rawData:
        
        lotNumber = row[0]
        orientationDate = row[3]
        cursor.execute('update BuilderTrendScrape set [Orientation Date] = ? where Lot = ?', orientationDate, lotNumber)
        cursor.commit()
        
    df = pd.read_sql("select [Lot Number], Title, [Start], [End] from BTScheduleRaw where Title like 'Dig Day'", engine)
    rawData = df.values.tolist()
    for row in rawData:
        
        lotNumber = row[0]
        digDay = row[3]
        cursor.execute('update BuilderTrendScrape set [Dig Day] = ? where Lot = ?', digDay, lotNumber)
        cursor.commit()
        
    df = pd.read_sql("select [Lot Number], Title, [Start], [End] from BTScheduleRaw where Title like 'Final Inspection'", engine)
    rawData = df.values.tolist()
    for row in rawData:
        
        lotNumber = row[0]
        cooDate = row[3]
        
        try:
            cooDate = datetime.datetime.strptime(digDay, '%b %d, %Y').date()
            cursor.execute('update BuilderTrendScrape set [Final Inspection COO Date] = ? where Lot = ?', cooDate, lotNumber)
        except Exception as ex:
            print("Here's the error: " + str(ex))
       
        cursor.commit()
        
    df = pd.read_sql("select Owner, [Lot Number] from BTSuperRaw", engine)
    rawData = df.values.tolist()
    for row in rawData:
        
        owner = row[0]
        lotNumber = row[1]
        
        try:
            cursor.execute('update BuilderTrendScrape set [Owner Name] = ? where Lot = ?', owner, lotNumber)
        except Exception as ex:
            print("Here's the error: " + str(ex))
    
        cursor.commit()
        
    try:
        cursor.execute('update BuilderTrendScrape set [Scraped On:] = ?', datetime.datetime.now())
    except Exception as ex:
        print("Here's the error: " + str(ex))
    
    cursor.commit()

    try:
        
        cursor.execute("update BuilderTrendScrape set [Job Name] = null where [Job Name] = 'nan'")
        cursor.execute("update BuilderTrendScrape set Lot = null where Lot = 'nan'")
        cursor.execute("update BuilderTrendScrape set [Owner Name] = null where [Owner Name] = 'nan'")
        cursor.execute("update BuilderTrendScrape set [Borrower Last Name] = null where [Borrower Last Name] = 'nan'")
        cursor.execute("update BuilderTrendScrape set [Co-Borrower First Name] = null where [Co-Borrower First Name] = 'nan'")
        cursor.execute("update BuilderTrendScrape set [Co-Borrower Last Name] = null where [Co-Borrower Last Name] = 'nan'")
        cursor.execute("update BuilderTrendScrape set [Street Address] = null where [Street Address] = 'nan'")
        cursor.execute("update BuilderTrendScrape set City = null where City = 'nan'")
        cursor.execute("update BuilderTrendScrape set ZIP = null where ZIP = 'nan'")
        #cursor.execute("update BuilderTrendScrape set [Project Manager] = null where [Project Manager] = 'nan'")
        cursor.execute("update BuilderTrendScrape set Owner = null where Owner = 'nan'")
        cursor.execute("update BuilderTrendScrape set Phone = null where Phone = 'nan'")
        cursor.execute("update BuilderTrendScrape set Email = null where Email = 'nan'")
        cursor.execute("update BuilderTrendScrape set [State] = null where [State] = 'nan'")

    except Exception as ex:
        print("Here's the error: " + str(ex))

    cursor.commit()