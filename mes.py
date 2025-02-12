import itauExcel as i
import pandas as pd
import pathlib as pl

def ArquivoExiste(path):
    file = pl.Path(path)
    return file.is_file()

def CarregarMes(diretorio, dataCobranca, ownerExcluido, log):
    arquivoDebito = diretorio + 'Extrato.xls'
    arquivoCredito = diretorio + 'Fatura-Excel.xls'
    arquivoPrevisoes = diretorio + 'Previsoes.csv'
    todasPlanilhas = []
       
    if (ArquivoExiste(arquivoDebito)):
        todasPlanilhas.append(i.Transform(i.ItauDebitoToDataFrame(arquivoDebito), 'Debito', None))
    else:
        log.error('Arquivo ' + arquivoDebito + ' não encontrado')
    if (ArquivoExiste(arquivoCredito)):
        todasPlanilhas.append(i.Transform(i.ItauCreditoToDataFrame(arquivoCredito), 'Credito', dataCobranca))
    else:
        log.error('Arquivo ' + arquivoCredito + ' não encontrado')
    if (ArquivoExiste(arquivoPrevisoes)):
        todasPlanilhas.append(i.Transform(i.ItauPrevisoesToDataFrame(arquivoPrevisoes), 'Previsoes', None))
    else:
        log.error('Arquivo ' + arquivoPrevisoes + ' não encontrado')
    if len(todasPlanilhas) == 0:
        log.error('Nenhuma planilha encontrada')
        return None, None
    
    total = pd.concat(todasPlanilhas, ignore_index=True)
    total = total.assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ',''))
    totalOwner = total.loc[total['Owner'].str.contains(ownerExcluido)]
    total = total.loc[~total['Owner'].str.contains(ownerExcluido)].sort_values(by='Date')
    return total, totalOwner
    
