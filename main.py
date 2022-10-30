import financesExcel as xls
import sqliteDb as db
import datetimeFunc as dt

def InitializeDb(dbConnection):
    db.CriarTabela(dbConnection,'Lancamentos', 
            [('EpochLancamento','int'), 
             ('TituloLancamento', 'text'), 
             ('CategoriaLancamento', 'text'), 
             ('ValorLancamento', 'real'), 
             ('PeriodoLancamento', 'text'), 
             ('OrigemLancamento', 'text'),
             ('DescricaoLancamento','text'),
             ('ParcelaAtual','int'),
             ('ParcelasTotais','int')],
             ',PRIMARY KEY (EpochLancamento, TituloLancamento, ValorLancamento)')


conn = db.ConnectToDatabase('finantialData.sqlite')
InitializeDb(conn)

d = xls.EstruturaExcelParaDataframe('./planilhas')
print(d)

db.SalvarDados(conn, d, 'Lancamentos')
db.DesconectarDoBanco(conn)
