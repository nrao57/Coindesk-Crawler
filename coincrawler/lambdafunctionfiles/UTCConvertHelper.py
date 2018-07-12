#Converts UTC Timestamp to Datetime and Datetime String
import datetime

def convFromUTC(ts):
    format_datetime = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(ts).strftime(format_datetime)
    
def convertToUTC(dtstring):
    dt = datetime.datetime.strptime(dtstring, '%Y-%m-%d')
    UTCtimestamp = (dt - datetime.datetime(1970, 1, 1)).total_seconds()
    return UTCtimestamp
    
def get_DateRange(rngstring):
    date1, date2 = rngstring.split('to')
    ts1 = convertToUTC(date1)
    ts2 = convertToUTC(date2)
    return ts1, ts2
