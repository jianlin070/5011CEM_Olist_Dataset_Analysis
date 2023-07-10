import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

df = pd.read_csv("olist_orders_dataset.csv")

status_counts = df['order_status'].value_counts()

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Order Status Distribution", style={'text-align': 'center'}),
    html.Div(
        html.Button("Reset Chart", id="reset-button", n_clicks=0),
        style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '60px'}
    ),
    html.Div(
        dcc.Graph(id='order-status-pie'),
        style={'display': 'flex', 'justify-content': 'center'}
    )
])

@app.callback(
    Output('order-status-pie', 'figure'),
    Input('reset-button', 'n_clicks'),
    State('order-status-pie', 'figure')
)
def reset_pie_chart(n_clicks, figure):
    fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, title='Order Status Distribution')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)