import sqlite3
from sqlite3 import Error
import pandas as pd
import logging as l

def SelectData(DbLiteFile, query):
    c = __ConnectToDatabase(DbLiteFile)
    df = __SelectData(c, query)
    __DisconnectFromDatabase(c)
    return df

def __ConnectToDatabase(DbLiteFile):
    sqlite3_conn = None
    try:
        sqlite3_conn = sqlite3.connect(DbLiteFile)
        return sqlite3_conn
    except Error as err:
        l.error(err)
        if sqlite3_conn is not None:
            sqlite3_conn.close()

def SaveData(DbLiteFile,dataFrame,table):
    c = __ConnectToDatabase(DbLiteFile)
    __SaveDataframe(c, dataFrame, table)
    __DisconnectFromDatabase(c)

def RemoveItemsInDatabase(DbLiteFile, DataFrame, Table):
    df = DataFrame
    for d in DataFrame:
         keyTuple = None
         for row in conn.execute("SELECT TransactionEpoch, TransactionAmount, TransactionTitle FROM Transactions " + 
                                 "WHERE TransactionEpoch = ? AND TransactionAmount = ? AND TransactionTitle = ?",
                                 (d['TransactionEpoch'], d['TransactionAmount'], d['TransactionTitle'])):
            if row[0] is not None:
                df.drop(d.index, inplace=True)

def __RowExists(conn,d):
    exists=False
    rows = conn.execute("SELECT TransactionEpoch, TransactionAmount, TransactionTitle FROM Transactions " + 
                        "WHERE TransactionEpoch = ? AND TransactionAmount = ? AND TransactionTitle = ?",
                        (d['TransactionEpoch'], d['TransactionAmount'], d['TransactionTitle']))
    for r in rows:
        exists=True
    return exists

def __MaskExists(conn, df):
    return pd.DataFrame({'mask': [__RowExists(conn, df.loc[i]) for i in range(len(df))]})

def __FullMask(m):
    return pd.DataFrame({'TransactionTitle': m,
                         'TransactionPeriod': m,
                         'TransactionOrigin': m,
                         'TransactionEpoch': m,
                         'TransactionAmount': m,
                         'TransactionCategory': m,
                         'TransactionDescription': m,
                         "CurrentInstallment": m,
                         "NumberOfInstallments": m,
                         "RecordCreationEpoch":m},index=m.index)

def InsertIfNotExist(dbLiteFile, df, table, UniqueColumns):
    conn = __ConnectToDatabase(dbLiteFile)
    df.reset_index(drop=True,inplace=True)
    m = __MaskExists(conn, df)
    print(m)
    d = df.where(__FullMask(m))
    print(d)
    print(d[d.TransactionTitle.notnull()])
    __DisconnectFromDatabase(conn)
# def __GenSelect(UniqueColumns):
#     return "SELECT " + ",".join(UniqueColumns)

#     the_id_of_the_row = None
# for row in sql.execute("SELECT id FROM foo WHERE data = ?", ...):
#     the_id_of_the_row = row[0]
# if the_id_of_the_row is None:
#     c = sql.cursor()
#     c.execute("INSERT INTO foo(data) VALUES(?)", ...)
#     the_id_of_the_row = c.lastrowid

def __SelectData(dbConnection, query):
    return pd.read_sql_query(query, dbConnection)

def __SaveDataframe(dbConnection, dataFrame, table):
    if dbConnection is not None:
        dataFrame.to_sql(name=table, con=dbConnection, if_exists='append', index=False)
        dbConnection.commit()

def __DisconnectFromDatabase(dbConnection):
    if dbConnection is not None:
        dbConnection.commit()

def __CreateTable(dbConnection, nomeTabela, campos, primaryKey):
    ccc = []
    [ccc.append(c[0] + ' ' + c[1]) for c in campos]
    colunas = ','.join(ccc)
    dbConnection.cursor().execute('Create table if not exists ' + nomeTabela + '(' + colunas + primaryKey + ');')