from datetime import datetime
import os

def ItauCreditoToDataFrame(xlsName):
    import pandas as pd
    import re
    df = pd.DataFrame(columns=['Date', 'Transaction', 'Amount', 'Owner'])
    owner = ""
    for index, row in pd.read_excel(xlsName, names=['A','B','C','D'], usecols='A:D').iterrows():
        if pd.notna(row['A']):
            x = re.search(r'^(.*) - final ([0-9]{4}) \(.*\)$', row['A'])
            if x:
                if "total" not in x.group(1):
                    owner = (x.group(1) + "(" + x.group(2) + ")")                    
                else:
                    owner = ""
            else:
                if (owner and "/" in row['A']) and ("dólar de conversão" not in row['B']) and pd.notna(row['D']):
                    df.loc[len(df)] = [row['A'], row['B'], row['D'], owner]
    return df

def ItauPrevisoesToDataFrame(csvNames):
    import pandas as pd
    import re
    df = pd.DataFrame(columns=['Date', 'Transaction', 'Amount', 'Owner'])
    owner = ""
    rd = pd.read_csv(csvNames)
    df['Date'] = rd['data']
    df['Transaction'] = rd['transacao']
    df['Amount'] = rd['valor']
    df['Owner'] = ""
    df = df.dropna(subset=['Amount']).dropna(subset=['Transaction']).dropna(subset=['Date'])

    return df

def ItauDebitoToDataFrame(xlsName):
    import pandas as pd
    import re
    df = pd.DataFrame(columns=['Date', 'Transaction', 'Amount', 'Owner'])
    owner = ""
    rd = pd.read_excel(xlsName, names=['A','B','C','D'], usecols='A:D')
    df['Date'] = rd['A']
    df['Transaction'] = rd['B']
    df['Amount'] = rd['D']
    df['Owner'] = ""
    df = df.dropna(subset=['Amount']).dropna(subset=['Transaction']).dropna(subset=['Date']).iloc[1:]

    return df

def GetTransactionTitleAndInstallments(strTransaction):
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

def Transform(dataFrame, origin, PaymentDate):
    import pandas as pd
    import datetimeFunc as dt
    return pd.DataFrame({'Title': [GetTransactionTitleAndInstallments(t)[0] for t in dataFrame.Transaction],
                         'Date': [dt.AdaptStrToDate(d) for d in dataFrame.Date],
                         'PaymentDate': [dt.AdaptStrToDate(d) for d in dataFrame.Date] if PaymentDate == None else datetime.strptime(PaymentDate, "%Y-%m-%d"),
                         'Amount': dataFrame.Amount * (-1 if origin == 'Credito' else 1),
                         'Origin': origin,
                         'Owner': dataFrame.Owner})

 