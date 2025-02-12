import time
from time import mktime
from datetime import datetime
import logging as l

def __PtBrMonthToNumber(mes):
    if (mes == 'janeiro'):
        return '01'
    elif (mes == 'fevereiro'):
        return '02'
    elif (mes == 'março' or mes == 'marco'):
        return '03'
    elif (mes == 'abril'):
        return '04'
    elif (mes == 'maio'):
        return '05'
    elif (mes == 'junho'):
        return '06'
    elif (mes == 'julho'):
        return '07'
    elif (mes == 'agosto'):
        return '08'
    elif (mes == 'setembro'):
        return '09'
    elif (mes == 'outubro'):
        return '10'
    elif (mes == 'novembro'):
        return '11'
    elif (mes == 'dezembro'):
        return '12'
    else:
        return ''

def AdaptDate(dataStr):
    l.info('AdaptDate ' + dataStr)
    return DateToEpoch(AdaptStrToDate(dataStr))

def AdaptStrToDate(dataStr):
    l.info('AdaptStrToDate ' + dataStr)
    return StrDateToDate(dataStr) if (dataStr.count('/') == 2) else StrDateFullToDate(dataStr)

def StrDateToDate(dataStr):
    l.info('StrDateToDate ' + dataStr)
    return datetime.strptime(dataStr, "%d/%m/%Y")

def DataParaDataStr(data):
    l.info('DataParaDataStr ' + dataStr)
    return datetime.strftime("%d/%m/%Y %H:%M",data)

def StrDateFullToDate(strDate):
    l.info('StrDateFullToDate ' + strDate)
    strDateSplit = strDate.split("/")
    currentDate = datetime.now()
    day = strDateSplit[0].strip()
    month = __PtBrMonthToNumber(strDateSplit[1].strip())
    l.info (strDateSplit[1].strip() + ' ' + month)
    year = currentDate.year
    date = DayMonthYearToDate(day,month,year)
    return DayMonthYearToDate(day,month,year -1) if (datetime.now() <= date) else date 

def DayMonthYearToDate(day, month, year):
    l.info('DayMonthYearToDate ' + str(day) + ' '+ str(month) + ' '+ str(year))
    return datetime.strptime(str(day)+ "/"+ str(month) + "/" + str(year), "%d/%m/%Y")

def DateToEpoch(date):
    epoch = (date - datetime(1970,1,1)).total_seconds() 
    l.info('DateToEpoch' + str(date) + '->' + str(epoch))
    return epoch

def EpochToDate(epoch):
    return datetime.fromtimestamp(mktime(time.localtime(epoch)))
