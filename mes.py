import itauExcel as i
import pandas as pd
import pathlib as pl
import loggerfactory as l

def ArquivoExiste(path):
    return pl.Path(path).is_file()

def CarregarMes(diretorio, dataCobranca, ownerExcluido):
    arquivoDebito = diretorio + 'Extrato.xls'
    arquivoCredito = diretorio + 'Fatura-Excel.xls'
    arquivoPrevisoes = diretorio + 'Previsoes.xls'
    todasPlanilhas = []
    
    log = l.getLogger(__name__)
       
    if (ArquivoExiste(arquivoDebito)):
        todasPlanilhas.append(i.Transform(i.ItauDebitoToDataFrame(arquivoDebito), 'Debito', None).assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ','')))
    else:
        log.error('Arquivo ' + arquivoDebito + ' não encontrado')
    if (ArquivoExiste(arquivoCredito)):
        todasPlanilhas.append(i.Transform(i.ItauCreditoToDataFrame(arquivoCredito), 'Credito', dataCobranca).assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ','')))
    else:
        log.error('Arquivo ' + arquivoCredito + ' não encontrado')
    if (ArquivoExiste(arquivoPrevisoes)):
        todasPlanilhas.append(i.Transform(i.ItauDebitoToDataFrame(arquivoPrevisoes), 'Previsoes', None).assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ','')))
    else:
        log.error('Arquivo ' + arquivoPrevisoes + ' não encontrado')
    if len(todasPlanilhas) == 0:
        log.error('Nenhuma planilha encontrada')
        return None, None
    total = pd.concat(todasPlanilhas, ignore_index=True)
    total = total.loc[~total['Owner'].str.contains(ownerExcluido)]
    totalOwner = total.loc[total['Owner'].str.contains(ownerExcluido)]
    return total, totalOwner
    
