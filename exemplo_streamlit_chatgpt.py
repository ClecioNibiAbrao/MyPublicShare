import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Simulação de dados
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
aeroportos = ['Aeroporto X', 'Aeroporto Y', 'Aeroporto Z']
companhias = ['Companhia A', 'Companhia B', 'Companhia C']
tipos = ['Chegada', 'Partida']
status = ['Atrasado', 'No Horário', 'Cancelado']

data = {
    'Data': np.random.choice(dates, 1000),
    'Aeroporto': np.random.choice(aeroportos, 1000),
    'Companhia': np.random.choice(companhias, 1000),
    'Tipo': np.random.choice(tipos, 1000),
    'Status': np.random.choice(status, 1000),
    'Passageiros': np.random.poisson(200, 1000)
}

df = pd.DataFrame(data)

# Criação do aplicativo Streamlit
st.set_page_config(page_title='Dashboard de Voos', layout='wide')

# Cabeçalho
st.title('Dashboard de Voos')

# Filtros
st.sidebar.header('Filtros')
aeroporto = st.sidebar.selectbox('Aeroporto:', ['Todos'] + aeroportos)
tipo = st.sidebar.selectbox('Tipo:', ['Todos'] + tipos)
status_filter = st.sidebar.selectbox('Status:', ['Todos'] + status)
companhia = st.sidebar.selectbox('Companhia:', ['Todos'] + companhias)
start_date = st.sidebar.date_input('Data de Início', datetime(2024, 1, 1))
end_date = st.sidebar.date_input('Data de Fim', datetime(2024, 12, 31))

if st.sidebar.button('Exportar CSV'):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(label='Download CSV', data=csv, file_name='dados_voos.csv', mime='text/csv')

# Filtrando o DataFrame com base nos filtros
filtered_df = df.copy()
if aeroporto != "Todos":
    filtered_df = filtered_df[filtered_df['Aeroporto'] == aeroporto]
if tipo != "Todos":
    filtered_df = filtered_df[filtered_df['Tipo'] == tipo]
if status_filter != "Todos":
    filtered_df = filtered_df[filtered_df['Status'] == status_filter]
if companhia != "Todos":
    filtered_df = filtered_df[filtered_df['Companhia'] == companhia]
if start_date is not None:
    filtered_df = filtered_df[filtered_df['Data'] >= pd.to_datetime(start_date)]
if end_date is not None:
    filtered_df = filtered_df[filtered_df['Data'] <= pd.to_datetime(end_date)]

# Gráfico de linha para passageiros
st.subheader('Número de Passageiros por Dia')
fig_passageiros = filtered_df.groupby('Data')['Passageiros'].sum().reset_index()
st.line_chart(data=fig_passageiros.set_index('Data')['Passageiros'], use_container_width=True)

# Gráfico de voos diários
st.subheader('Voos Diários (Entradas e Saídas)')
voos_diarios_filtrados = filtered_df.groupby(['Data', 'Tipo']).size().unstack(fill_value=0).reset_index()
voos_diarios_filtrados.columns.name = None
voos_diarios_filtrados = voos_diarios_filtrados.reindex(columns=['Data', 'Chegada', 'Partida'], fill_value=0)
voos_diarios_filtrados.rename(columns={'Chegada': 'Voos_Chegada', 'Partida': 'Voos_Partida'}, inplace=True)

st.bar_chart(data=voos_diarios_filtrados.set_index('Data')[['Voos_Chegada', 'Voos_Partida']], use_container_width=True)

# Exibir tabela de dados filtrados
st.subheader('Tabela de Dados Filtrados')
st.write(filtered_df)

# Instruções para exportar CSV
if st.sidebar.button('Exportar CSV'):
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(label='Download CSV', data=csv, file_name='dados_voos.csv', mime='text/csv')
