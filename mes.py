import itauExcel as i
import pandas as pd
import pathlib as pl
from dataclasses import dataclass

@dataclass
class MonthExpense:
    month: str
    total: pd.DataFrame
    totalOwner: pd.DataFrame


def ArquivoExiste(path):
    file = pl.Path(path)
    return file.is_file()

def CarregarMes(diretorio, ano, mes, ownerExcluido, log):
    fullpath = diretorio + ano  + '/' + mes + '/'
    arquivoDebito = fullpath + 'Extrato.xls'
    arquivoCredito = fullpath + 'Fatura-Excel.xls'
    arquivoPrevisoes = fullpath + 'Previsoes.csv'
    todasPlanilhas = []
       
    if (ArquivoExiste(arquivoDebito)):
        todasPlanilhas.append(i.Transform(i.ItauDebitoToDataFrame(arquivoDebito), 'Debito', None))
    else:
        log.error('Arquivo ' + arquivoDebito + ' não encontrado')
    if (ArquivoExiste(arquivoCredito)):
        todasPlanilhas.append(i.Transform(i.ItauCreditoToDataFrame(arquivoCredito), 'Credito', ano + '-' + mes + '-09'))
    else:
        log.error('Arquivo ' + arquivoCredito + ' não encontrado')
    if (ArquivoExiste(arquivoPrevisoes)):
        f = i.Transform(i.ItauPrevisoesToDataFrame(arquivoPrevisoes), 'Previsoes', None)
        log.fatal(f)
        todasPlanilhas.append(f)
    else:
        log.error('Arquivo ' + arquivoPrevisoes + ' não encontrado')
    if len(todasPlanilhas) == 0:
        log.error('Nenhuma planilha encontrada')
        return MonthExpense(mes + '/' + ano, None, None)
    
    total = pd.concat(todasPlanilhas, ignore_index=True)
    total = total.assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ',''))
    totalOwner = total.loc[total['Owner'].str.contains(ownerExcluido)]
    total = total.loc[~total['Owner'].str.contains(ownerExcluido)].sort_values(by='Date')
    return MonthExpense(mes + '/' + ano, total, totalOwner)
    
