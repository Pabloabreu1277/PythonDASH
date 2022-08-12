# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# https://dash.plotly.com/layout
# pip install pandas
# pip install dash
# pip install plotly
# pip install openpyxl
from dash import Dash, html, dcc, Input,Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

opcoes = list(df['ID Loja'].unique())
opcoes.append("Todas as Lojas")


# HTML
app.layout = html.Div(children=[
    html.H1(children='Dashboard Vendas'),
    html.H1(children='Grafico com o faturamento de todos os produtos separados por loja'),
    html.Button("Download Excel", id="btn_xlsx"),

    html.Div(children='''
        Esse grafico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),

# Dashboard
    dcc.Download(id="download-dataframe-xlsx"),
    dcc.Dropdown(opcoes, value='Todas as Lojas', id='Lista de lojas'),

    dcc.Graph(
        id='Grafico_Quantidade_Vendas',
        figure=fig
    )
])

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
@app.callback(
    Output('Grafico_Quantidade_Vendas', 'figure'), #saidas o que vai mudas e que parametro vou alterar na tela
    Input('Lista de lojas', 'value') #entradas o que vou editar e a referencia
)

def update_output(value):
    if value=='Todas as Lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

    return fig

def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")


if __name__ == '__main__':
    app.run_server(debug=True)