import streamlit as st
import itauExcel as i
import pandas as pd
import summary as s
import categorias as cat
import mes as m
import loggerfactory as l

log = l.getLogger(__name__)

baseDir = '~/Documents/Planilhas/'
categories = cat.CarregarCategorias(baseDir)
meses = []
mesesAlice = []
datas = ['2025-01-09', '2025-02-09', '2025-03-09', '2025-04-09', '2025-05-09', '2025-06-09']
count = 0
for i in ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho']:
    log.error('Carregando ' + i + ' ' + str(count))
    total, totalAlice = m.CarregarMes('~/Documents/Planilhas/' + '2025/' + i + '/', datas[count], 'ALICE')    
    log.error("1")
    if total is not None:
        meses.append(total)
    log.error("2")
    if totalAlice is not None:
        mesesAlice.append(totalAlice)
    log.error("3")
    count = count + 1
    log.error("4")  

gastos = pd.concat(meses, ignore_index=True)

gastos_categorizados = pd.merge(gastos, categories, on='Title_Merge', how='left')
st.divider()
st.write(creditoAlice['Amount'].sum())
st.divider()

precisa_categorizar = gastos_categorizados.loc[gastos_categorizados['Category'].isnull(), 'Title'].unique()
st.write(precisa_categorizar)
titulo = st.selectbox('Select a title', precisa_categorizar)
st.write(gastos_categorizados.loc[gastos_categorizados['Title'] == titulo])

# Two equal columns:
col1, col2 = st.columns(2)
col1.write("This is column 1")
col2.write("This is column 2")

# Three different columns:
col1, col2, col3 = st.columns([3, 1, 1])
# col1 is larger.

# Bottom-aligned columns
col1, col2 = st.columns(2, vertical_alignment="bottom")

# You can also use "with" notation:
with col1:
    st.radio("Select one:", [1, 2])

st.write("This is column 1")

tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
    st.write("this is tab 1")



gastos_categorizados['Category'] = gastos_categorizados['Category'].fillna('?')
gastos_categorizados['Amount'] = abs(gastos_categorizados['Amount'])

s.GraficoPizza(gastos_categorizados)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

st.text("Fixed width text")
st.markdown("_Markdown_")
st.latex(r""" e^{i\pi} + 1 = 0 """)
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")
st.html("<p>Hi!</p>")

with st.echo():
    st.write("Code will be executed and printed")

