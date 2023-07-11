import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Dash

# Load the CSV data
df_orders = pd.read_csv("olist_orders_dataset.csv")

orders_upd = df_orders.copy()
orders_upd["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"], format='%Y-%m-%d %H:%M:%S')
orders_upd["order_delivered_carrier_date"] = pd.to_datetime(df_orders["order_delivered_carrier_date"], format='%Y-%m-%d %H:%M:%S')
orders_upd["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"], format='%Y-%m-%d %H:%M:%S')
orders_upd["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"], format='%Y-%m-%d %H:%M:%S')

# Count the total number of orders per day
order_counts = orders_upd.set_index("order_purchase_timestamp").resample('D').count()

# Create the Dash app
app = Dash(__name__)

# Set up the layout
app.layout = html.Div(
    children=[
        html.H1("Olist Order History"),
        dcc.Graph(
            id="order-graph",
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=order_counts.index,
                        y=order_counts['order_id'],
                        mode='lines',
                        name='Total Orders'
                    )
                ],
                layout=go.Layout(
                    title='Number of Orders per day',
                    xaxis={'title': 'Order Purchase Date'},
                    yaxis={'title': 'Total Orders'}
                )
            )
        )
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
