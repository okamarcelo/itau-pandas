import streamlit as st
import itauExcel as i
import pandas as pd
import summary as s
import categorias as cat
import mes as m
import loggerfactory as l
from datetime import timedelta, datetime

log = l.getLogger("")

baseDir = '~/Documents/Planilhas/'
categories = cat.CarregarCategorias(baseDir)
meses = []
for item in ['1', '2', '3', '4', '5', '6']:
    meses.append(m.CarregarMes('/home/okamarcelo/Documents/Planilhas/', '2025', item, 'ALICE', log))



        #st.header(nome_mes)


            #st.write("Gastos cartão Alice:" + str(abs(totalAlice['Amount'].sum())))
            #s.GraficoPizza(total_cat)
gastos = pd.concat((mes.total for mes in meses), ignore_index=True)
gastos= pd.merge(gastos, categories, on='Title_Merge', how='left')
#
saldo_mp = 2013.83
saldo_itau = 1684.79
data_ini = datetime.strptime('2025-03-01', "%Y-%m-%d")

data_fim = st.date_input("Data fim", value='2025-05-10')
data_fim = str(data_fim)
data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
saldo_ini = saldo_mp + saldo_itau
val_prev_credito = -951.31
data_x = datetime.strptime('2025-03-09' , "%Y-%m-%d")
gastos = gastos.loc[(gastos['PaymentDate'] >= data_ini) & (gastos['PaymentDate'] <= data_fim)]
gastos.loc[len(gastos)] = ['SALDO INICIAL', data_ini - timedelta(days=1), data_ini - timedelta(days=1), saldo_ini, '', '', '', '']
gastos.loc[len(gastos)] = ['PREVISAO CREDITO', data_x, data_x, val_prev_credito, '', '', '', '']

s.YearSummary(gastos)
    
st.sidebar.slider(
     'Select a range of values',
     data_ini, data_ini + timedelta(days=30))

##gastos.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['Amount'])


# precisa_categorizar = gastos.loc[gastos['Category'] == '?', 'Title'].unique()
# st.write(precisa_categorizar)
# titulo = st.selectbox('Select a title', precisa_categorizar)
# st.write(gastos.loc[gastos['Title'] == titulo])

# # Two equal columns:
# col1, col2 = st.columns(2)
# col1.write("This is column 1")
# col2.write("This is column 2")
# 
# # Three different columns:
# col1, col2, col3 = st.columns([3, 1, 1])
# # col1 is larger.
# 
# # Bottom-aligned columns
# col1, col2 = st.columns(2, vertical_alignment="bottom")
# 
# # You can also use "with" notation:
# with col1:
#     st.radio("Select one:", [1, 2])
# 
# st.write("This is column 1")
# 
# tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
# tab1.write("this is tab 1")
# tab2.write("this is tab 2")
# 
# # You can also use "with" notation:
# with tab1:
#     st.write("this is tab 1")
# 
# 
# 
# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )
# 
# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )
# 
# st.text("Fixed width text")
# st.markdown("_Markdown_")
# st.latex(r""" e^{i\pi} + 1 = 0 """)
# st.title("My title")
# st.header("My header")
# st.subheader("My sub")
# st.code("for i in range(8): foo()")
# st.html("<p>Hi!</p>")
# 
# with st.echo():
#     st.write("Code will be executed and printed")

