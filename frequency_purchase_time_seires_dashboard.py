import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# Load the data
order = pd.read_excel('Olist_dataset.xlsx', sheet_name='orders')
order_items = pd.read_excel('Olist_dataset.xlsx', sheet_name='order_items')
products = pd.read_excel('Olist_dataset.xlsx', sheet_name='products')

# Merge the data
ord_prod = pd.merge(order_items, products, on="product_id", how="outer", indicator=True)
ord_final = pd.merge(order, ord_prod, on="order_id", how="outer")
ord_final = ord_final.drop({'_merge'}, axis='columns')

# Group by purchase timestamp and count the number of orders
ord_group_quant = ord_final.groupby('order_purchase_timestamp').count()['order_id'].reset_index()

fig1 = px.line(ord_group_quant, x='order_purchase_timestamp', y='order_id',
               title='Frequency of purchases per day',
               labels={'order_purchase_timestamp': 'Year / Month', 'order_id': 'Quantity'})

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Frequency of Purchase Per Day'),
    dcc.Graph(figure=fig1)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
