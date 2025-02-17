import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def GraficoPizza(dados_categorizados):
    dados_categorizados['Category'] = dados_categorizados['Category'].fillna('?')
    st.divider()
    st.header('')    
    pivot = dados_categorizados.pivot_table(index= 'Category', aggfunc='sum', values='Amount').sort_values(by='Amount', ascending=False)
    gastos = pivot.loc[pivot['Amount'] < 0, 'Amount']
    gastos = abs(gastos)
    rendimentos = pivot.loc[pivot['Amount'] > 0, 'Amount']
    rendimentos = abs(rendimentos)
    fig, ax = plt.subplots()
    st.write(rendimentos.sum() - gastos.sum())
    st.bar_chart(pd.DataFrame({'Gastos': [gastos.sum()], 'Rendimentos': [rendimentos.sum()]}), stack=False)
    ax = gastos.plot.pie(title=None,y='Amount', autopct='%1.1f%%', ax=ax, legend=None, rotatelabels=True, ylabel='', colormap='cool')
    st.pyplot(fig)
    st.write(gastos)
    categorias = dados_categorizados['Category'].unique()    
    st.write(dados_categorizados.loc[dados_categorizados['Category'] == st.selectbox('Visualizar Categoria', categorias), ['Date', 'Title', 'Amount', 'Owner']])
    
