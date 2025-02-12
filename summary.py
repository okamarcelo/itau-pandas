import streamlit as sl
import matplotlib.pyplot as plt

def GraficoPizza(dados_categorizados):
    dados_categorizados['Category'] = dados_categorizados['Category'].fillna('?')
    dados_categorizados['Amount'] = abs(dados_categorizados['Amount'])
    sl.divider()
    sl.header('')
    pivot = dados_categorizados.pivot_table(index= 'Category', aggfunc='sum', values='Amount').sort_values(by='Amount', ascending=False)
    fig, ax = plt.subplots()
    gastos = 0
    rendimentos = 0
    ax = pivot.plot.pie(title=None,y='Amount', autopct='%1.1f%%', ax=ax, legend=None, rotatelabels=True, ylabel='', colormap='cool')
    sl.pyplot(fig)
    sl.write(ax)
    sl.write(pivot)
    categorias = dados_categorizados['Category'].unique()    
    sl.write(dados_categorizados.loc[dados_categorizados['Category'] == sl.selectbox('Visualizar Categoria', categorias), ['Date', 'Title', 'Amount', 'Owner']])
    sl.divider()
