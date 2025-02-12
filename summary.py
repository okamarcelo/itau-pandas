import streamlit as sl
import matplotlib.pyplot as plt

def GraficoPizza(dados_categorizados):
    sl.divider()
    sl.header('Gastos por Categoria')
    pivot = dados_categorizados.pivot_table(index= 'Category', aggfunc='sum', values='Amount')
    fig, ax = plt.subplots()
    ax = pivot.plot.pie(title=None,y='Amount', autopct='%1.1f%%', ax=ax, legend=None, rotatelabels=True, ylabel='', colormap='cool')
    sl.pyplot(fig)
    sl.write(ax)
    sl.write(pivot)
    categorias = dados_categorizados['Category'].unique()    
    sl.write(dados_categorizados.loc[dados_categorizados['Category'] == sl.selectbox('Visualizar Categoria', categorias), ['Date', 'Title', 'Amount', 'Owner']])
    sl.divider()
