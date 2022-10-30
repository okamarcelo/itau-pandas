import sqlite3
from sqlite3 import Error
import pandas as pd
import logging as l

def SelectData(DbLiteFile, query):
    c = __ConectToDatabase(NomeArquivoDblite)
    df = __SelectData(c, query)
    __DisconnectFromDatabase(c)
    return df

def __ConectToDatabase(NomeArquivoDblite):
    sqlite3_conn = None
    try:
        sqlite3_conn = sqlite3.connect(NomeArquivoDblite)
        return sqlite3_conn
    except Error as err:
        l.error(err)
        if sqlite3_conn is not None:
            sqlite3_conn.close()

def __SelectData(dbConnection, query):
    return pd.read_sql_query(query, dbConnection)

def __SaveData(dbConnection, dataFrame, table):
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