import pandas as pd
import os
#from datetime import timestamp
import datetimeFunc as dt
import logging as l

def ExportExcel(fileName, dataFrame):
    df = pd.DataFrame({'Date': [ dt.EpochToDate(d) for d in dataFrame.TransactionEpoch], 
                  'Transaction': dataFrame.TransactionTitle, 
                  'Category': dataFrame.TransactionCategory, 
                  'Amount': dataFrame.TransactionAmount,
                  'Period': dataFrame.TransactionPeriod,
                  'Current Installment': dataFrame.CurrentInstallment,
                  'Total Installments': dataFrame.NumberOfInstallments})
    Periods = df.Period.unique()
    l.info(Periods)
    with pd.ExcelWriter(fileName) as writer:
        for Period in Periods:
            df[df.Period == Period].to_excel(writer, index=None, sheet_name=Period)

def __ReadExcel(xlsName):
    d = pd.read_excel(xlsName, names=['Date', 'Transaction', 'Category', 'Amount'], usecols='A:D')
    d = d[d.Date.str.contains("/", na=False) & d.Amount.notnull()]
    return d 

def __GetTransactionTitleAndInstallments(strTransaction):
    if "/" in strTransaction:
        s = strTransaction.replace("(","").replace(")","")
        ss = s.split("/")
        totalInstallments = ss[1]
        currentInstallment = ss[0][-2:]
        transactionTitle = ss[0][0:-2].strip()
        if (len(transactionTitle) > 18):
            transactionTitle = transactionTitle[0:18]
        r = (transactionTitle,currentInstallment,totalInstallments)
        return r
    else:
        return (strTransaction,None,None)

def __Transform(dataFrame, period, origin):
    return pd.DataFrame({'TransactionTitle': [__GetTransactionTitleAndInstallments(t)[0] for t in dataFrame.Transaction],
                         'TransactionPeriod': period,
                         'TransactionOrigin': origin,
                         'TransactionEpoch': [dt.AdaptDate(d) + 3600 * 3 for d in dataFrame.Date],
                         'TransactionAmount': dataFrame.Amount * (-1 if origin == 'Credito' else 1),
                         'TransactionCategory': dataFrame.Category,
                         'TransactionDescription': '',
                         "CurrentInstallment": [__GetTransactionTitleAndInstallments(t)[1] for t in dataFrame.Transaction],
                         "NumberOfInstallments": [__GetTransactionTitleAndInstallments(t)[2] for t in dataFrame.Transaction],
                         "RecordCreationEpoch":''})#dt.DateToEpoch(timestamp.today())})

def __GenerateDuplicateMask(dataFrame):
    return dataFrame.duplicated(subset=['TransactionEpoch','TransactionAmount','TransactionTitle'])

def __NormalizeDuplicates(dataFrame):
    dataFrame.TransactionEpoch = dataFrame.TransactionEpoch.where(~__GenerateDuplicateMask(dataFrame), dataFrame.TransactionEpoch + 1)
    return dataFrame

def __FixDuplicates(dataFrame):
    dd = __GenerateDuplicateMask(dataFrame)
    while dd.any():
        l.warn('duplicates found')
        dataFrame = __NormalizeDuplicates(dataFrame)
        dd = __GenerateDuplicateMask(dataFrame)
    return dataFrame

def __LocateSheets(rootDir):
    lista = []
    for root, dirs, files in os.walk(rootDir):
        for f in files:
            fullpath = os.path.abspath(os.path.join(root,f))
            print(fullpath)
            splitpath = fullpath.split('\\')
            arquivo = splitpath.pop()
            diretorio = splitpath.pop()
            lista.append((fullpath,arquivo.split('.')[0], diretorio))
    return lista

def ImportExcel(arquivo,periodoLancamento,origemLancamento):
    return __FixDuplicates(__Transform(__ReadExcel(arquivo),periodoLancamento,origemLancamento))

def EstruturaExcelParaDataframe(sheetsPath):
    d = pd.DataFrame(columns = ["TransactionTitle", "TransactionPeriod", "TransactionOrigin","TransactionEpoch","TransactionAmount","TransactionCategory", "CurrentInstallment", "NumberOfInstallments" ,"RecordCreationEpoch"])
    for p in __LocateSheets(sheetsPath):
        d.append(ImportExcel(p[0],p[1],p[2]))
    return d
