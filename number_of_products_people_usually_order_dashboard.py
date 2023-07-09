# Import packages
from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objs as go

# Incorporate data
order = pd.read_csv('olist_order_items_dataset.csv')

order_usual = order.groupby('order_id')['order_item_id'].aggregate('sum').reset_index()
order_usual = order_usual['order_item_id'].value_counts()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={'display': 'flex', 'justify-content': 'center'},
    children=[
        html.Div(
            style={'width': '60%'},
            children=[
                html.H1("Number of products people usually order", style={'text-align': 'center'}),
                dcc.Graph(
                    id='bar-chart',
                    figure={
                        'data': [
                            go.Bar(
                                x=order_usual.index,
                                y=order_usual.values,
                                marker={'color': 'green'},
                                width=1
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Number of products added in order',
                                   'range': [0, 20],
                                   'tickmode': 'linear',
                                   'dtick': 1},
                            yaxis={'title': 'Number of orders'},
                            height=800,
                            width=1000,
                            bargap=0.1,
                            title='Number of products people usually order',
                            xaxis_tickangle=-90
                        )
                    }
                )
            ]
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)