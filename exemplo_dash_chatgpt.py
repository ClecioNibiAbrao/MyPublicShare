import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# Criação do aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'black', 'color': 'white'}, children=[
    html.H1('Dashboard de Voos', style={'textAlign': 'center'}),
    
    # Filtros
    html.Div([
        html.Label('Aeroporto:'),
        dcc.Dropdown(
            id='aeroporto-dropdown',
            options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': a, 'value': a} for a in aeroportos],
            value='Todos'
        ),
        html.Label('Tipo:'),
        dcc.Dropdown(
            id='tipo-dropdown',
            options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': t, 'value': t} for t in tipos],
            value='Todos'
        ),
        html.Label('Status:'),
        dcc.Dropdown(
            id='status-dropdown',
            options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': s, 'value': s} for s in status],
            value='Todos'
        ),
        html.Label('Companhia:'),
        dcc.Dropdown(
            id='companhia-dropdown',
            options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': c, 'value': c} for c in companhias],
            value='Todos'
        ),
        html.Label('Período:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
            display_format='DD/MM/YYYY'
        ),
        html.Button('Exportar CSV', id='export-csv', n_clicks=0)
    ], style={'display': 'flex', 'gap': '15px', 'backgroundColor': '#333333', 'padding': '10px', 'borderRadius': '5px'}),
    
    # Gráficos
    dcc.Graph(id='passageiros-graph'),
    dcc.Graph(id='voos-diarios-graph'),
    
    # Componente para download
    dcc.Download(id='download-dataframe-csv')
])

@app.callback(
    [Output('passageiros-graph', 'figure'),
     Output('voos-diarios-graph', 'figure'),
     Output('download-dataframe-csv', 'data')],
    [Input('aeroporto-dropdown', 'value'),
     Input('tipo-dropdown', 'value'),
     Input('status-dropdown', 'value'),
     Input('companhia-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('export-csv', 'n_clicks')]
)
def update_output(aeroporto, tipo, status, companhia, start_date, end_date, n_clicks):
    # Filtrando o DataFrame com base nos filtros
    filtered_df = df.copy()
    if aeroporto != "Todos":
        filtered_df = filtered_df[filtered_df['Aeroporto'] == aeroporto]
    if tipo != "Todos":
        filtered_df = filtered_df[filtered_df['Tipo'] == tipo]
    if status != "Todos":
        filtered_df = filtered_df[filtered_df['Status'] == status]
    if companhia != "Todos":
        filtered_df = filtered_df[filtered_df['Companhia'] == companhia]
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['Data'] >= start_date]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['Data'] <= end_date]

    # Gráfico de linha para passageiros
    filtered_df_sorted = filtered_df.sort_values(by='Data')  # Ordenar o DataFrame por data
    fig_passageiros = {
        'data': [{
            'x': filtered_df_sorted['Data'],
            'y': filtered_df_sorted['Passageiros'],
            'type': 'line',
            'name': 'Passageiros',
            'line': {'color': 'cyan'}
        }],
        'layout': {
            'title': 'Número de Passageiros por Dia',
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font': {'color': 'white'},
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Número de Passageiros'}
        }
    }

    # Contagem de voos diários com base nos filtros
    voos_diarios_filtrados = filtered_df.groupby(['Data', 'Tipo']).size().unstack(fill_value=0).reset_index()
    voos_diarios_filtrados.columns.name = None

    # Garantindo que as colunas "Chegada" e "Partida" existam
    voos_diarios_filtrados = voos_diarios_filtrados.reindex(columns=['Data', 'Chegada', 'Partida'], fill_value=0)
    voos_diarios_filtrados.rename(columns={'Chegada': 'Voos_Chegada', 'Partida': 'Voos_Partida'}, inplace=True)

    # Gráfico de barras para voos diários
    fig_voos_diarios = {
        'data': [
            {'x': voos_diarios_filtrados['Data'], 'y': voos_diarios_filtrados['Voos_Partida'], 'type': 'bar', 'name': 'Voos de Partida', 'marker': {'color': '#1f77b4'}},
            {'x': voos_diarios_filtrados['Data'], 'y': voos_diarios_filtrados['Voos_Chegada'], 'type': 'bar', 'name': 'Voos de Chegada', 'marker': {'color': '#ff7f0e'}}
        ],
        'layout': {
            'title': 'Voos Diários (Entradas e Saídas)',
            'barmode': 'group',
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font': {'color': 'white'},
            'yaxis': {'title': 'Quantidade de Voos'},
            'xaxis': {'title': 'Data'}
        }
    }

    # Dados para exportação
    if n_clicks > 0:
        return fig_passageiros, fig_voos_diarios, dcc.send_data_frame(filtered_df.to_csv, "dados_voos.csv", index=False)

    return fig_passageiros, fig_voos_diarios, None

if __name__ == '__main__':
    app.run_server(debug=True)
