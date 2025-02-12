import pandas as pd

def CarregarCategorias(diretorio):
    return pd.read_csv(diretorio + 'categorias.csv').assign(Title_Merge=lambda row: row.Title.str.strip().str.upper().str.replace(' ','') ).filter(['Title_Merge', 'Category'])