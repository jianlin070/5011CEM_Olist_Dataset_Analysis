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

# Create the first plot - Total amount per day
ord_group_price = ord_final.groupby(ord_final['order_purchase_timestamp']).sum()['price'].reset_index()

fig1 = px.line(ord_group_price, x='order_purchase_timestamp', y='price',
               title='Total amount per day',
               labels={'order_purchase_timestamp': 'Year / Month', 'price': 'Total Value'})

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Total Amount Per Day'),
    dcc.Graph(figure=fig1)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
