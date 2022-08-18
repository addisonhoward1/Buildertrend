def ClearingTables(engine):
    try:
        engine.connect().execute("drop table BTSuperRaw")
    except Exception as ex:
        print("Here's the error: " + str(ex))
        
    try:
        engine.connect().execute("drop table BTScheduleRaw")
    except Exception as ex:
        print("Here's the error: " + str(ex))