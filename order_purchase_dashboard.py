import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px

orders = pd.read_csv("olist_orders_dataset.csv")
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], format='%Y-%m-%d %H:%M:%S')

orders_per_month = orders.groupby(pd.Grouper(key='order_purchase_timestamp', freq='M')).size().reset_index(name='Number of Orders')

app = dash.Dash()

app.layout = html.Div(
    children=[
        dcc.Graph(
            figure=px.histogram(
                orders_per_month,
                x='order_purchase_timestamp',
                y='Number of Orders',
                nbins=len(orders_per_month),
                title='Number of Orders per month'
            )
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
