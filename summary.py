import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
import altair as alt

def MonthSummary(dados_categorizados):
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
    
def YearSummary(dados_categorizados):
    gastos = dados_categorizados.reset_index(drop=True).reindex(columns=['Title','PaymentDate', 'Date', 'Amount', 'Owner', 'Origin', 'Category']).sort_values(by=['PaymentDate','Date'] )
    st.write(gastos)
    summary = gastos[['PaymentDate', 'Amount']].groupby('PaymentDate', as_index = False).sum().assign(Acumulado = lambda x: x['Amount'].cumsum()).sort_values(by='PaymentDate')
    new_df = pd.DataFrame(columns=['PaymentDate','Amount', 'Acumulado'])
    for index, row in summary.iterrows():
        transpose_row = pd.DataFrame(row).T
        if len(new_df) == 0:
            new_df = transpose_row
        else:
            while new_df.iloc[-1].PaymentDate + timedelta(days=1) != row.PaymentDate:
                var = pd.DataFrame(columns=['PaymentDate','Amount', 'Acumulado'],)
                var['PaymentDate'] = [new_df.iloc[-1].PaymentDate + timedelta(days=1)]
                var['Amount'] = 0
                var['Acumulado'] = new_df.iloc[-1].Acumulado
                new_df = pd.concat([new_df, var], ignore_index=True)
            new_df = pd.concat([new_df, pd.DataFrame(transpose_row)], ignore_index=True)
    new_df.set_index('PaymentDate', inplace=True)
    st.bar_chart(new_df['Acumulado'])
    source = pd.DataFrame({
        "Day": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "Value": [55, 112, 65, 38, 80, 138, 120, 103, 395, 200, 72, 51, 112, 175, 131]
    })
    threshold = 300

    bars = alt.Chart(source).mark_bar(color="steelblue").encode(
        x="Day:O",
        y="Value:Q",
    )
  
    highlight = bars.mark_bar(color="#e45755").encode(
        y2=alt.Y2(datum=threshold)
    ).transform_filter(
        alt.datum.Value > threshold
    )

    rule = alt.Chart().mark_rule().encode(
        y=alt.Y(datum=threshold)
    )

    label = rule.mark_text(
        x="width",
        dx=-2,
        align="right",
        baseline="bottom",
        text="hazardous"
    )

    st.altair_chart(bars + highlight + rule + label)


    
    #x='year:O',y='sum(yield):Q',color='year:N',column='site:N'

    
