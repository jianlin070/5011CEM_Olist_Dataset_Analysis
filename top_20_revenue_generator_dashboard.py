import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from dash import Dash,dcc, html

# Reading all the tables
df = pd.read_excel('Olist_dataset.xlsx')
order = pd.read_excel('Olist_dataset.xlsx', sheet_name='orders')
order_items = pd.read_excel('Olist_dataset.xlsx', sheet_name='order_items')
customers = pd.read_excel('Olist_dataset.xlsx', sheet_name='customers')
payments = pd.read_excel('Olist_dataset.xlsx', sheet_name='payments')
products = pd.read_excel('Olist_dataset.xlsx', sheet_name='products')

ord_prod = pd.merge(order_items, products, on="product_id", how="outer", indicator=True)
cust_ord = pd.merge(order, customers, on="customer_id", how="outer", indicator=True)
ord_pay = pd.merge(cust_ord, payments, on="order_id", how="outer")
ord_final = pd.merge(ord_pay, ord_prod, on="order_id", how="outer")
ord_final = ord_final.drop({'_merge_x', '_merge_y'}, axis='columns')

prod_rev = ord_final.groupby(by=["product_category_name"])["price"].sum()
a = pd.DataFrame(prod_rev.nlargest(20)).reset_index()

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Top 20 Revenue Generator', style={'text-align': 'center'}),

    dcc.Graph(
        id='revenue-bar-chart',
        figure={
            'data': [
                {'x': a['product_category_name'], 'y': a['price'], 'type': 'bar'}
            ],
            'layout': {
                'title': 'Top 20 Revenue Generator',
                'yaxis': {'title': 'Revenue'},
                'xaxis': {'title': 'Category'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
