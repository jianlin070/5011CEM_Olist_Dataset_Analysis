
import warnings
warnings.filterwarnings('ignore')

# Importing the required libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt
from sklearn.decomposition import TruncatedSVD

import dash
import dash_html_components as html
import dash_core_components as dcc

# Reading all the tables
df = pd.read_excel (r'Olist_dataset.xlsx')
order = pd.read_excel (r'Olist_dataset.xlsx', sheet_name='orders')
order_items = pd.read_excel (r'Olist_dataset.xlsx', sheet_name='order_items')
customers = pd.read_excel (r'Olist_dataset.xlsx', sheet_name='customers')
payments = pd.read_excel (r'Olist_dataset.xlsx', sheet_name='payments')
products = pd.read_excel (r'Olist_dataset.xlsx', sheet_name='products')

# we have taken median of differences between order_approved_at and order_purchased and then filled the nan values with sum of order_purchased and diff
diff = (order['order_approved_at'] - order['order_purchase_timestamp']).median()
order['order_approved_at'].fillna(order['order_purchase_timestamp'] + diff,inplace=True)

# we have taken median of differences between order_delivered_carrier_date and order_approved_at and then filled the nan values with sum of order_approved_at and diff
diff = (order['order_delivered_timestamp'] - order['order_approved_at']).median()
order['order_delivered_timestamp'].fillna(order['order_approved_at'] + diff,inplace=True)

# creating one more column delayed or not where 0=within time and 1=delayed
order['delayed'] = np.where(order['order_delivered_timestamp']>order['order_estimated_delivery_date'],1,0)

# creating new column ie. delivery time duration = time duration between delivered to customer date and purchase timestamp
order['delivery_time_duration'] = order['order_delivered_timestamp'] - order['order_purchase_timestamp']

cust_ord =pd.merge(order, customers, on="customer_id", how="outer", indicator=True)

ord_pay = pd.merge(cust_ord, payments, on="order_id", how="outer")
ord_prod = pd.merge(order_items, products, on="product_id", how="outer", indicator=True)

ord_final = pd.merge(ord_pay, ord_prod, on="order_id", how="outer")
ord_final = ord_final.drop({'_merge_x','_merge_y'},axis='columns')


null_lead = pd.DataFrame((ord_final.isnull().sum())*100/ord_final.shape[0]).reset_index()


# Creating the Dash application
app = dash.Dash(__name__)

# Defining the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Percentage of Missing Values"),
        dcc.Graph(
            id="missing-values-graph",
            figure={
                'data': [{
                    'x': null_lead["index"],
                    'y': null_lead[0],
                    'type': 'scatter',
                    'mode': 'lines+markers',
                    'marker': {'color': 'blue'}
                }],
                'layout': {
                    'title': 'Percentage of Missing Values',
                    'xaxis': {'title': 'Columns'},
                    'yaxis': {'title': 'Percentage', 'range': [0, 50], 'dtick': 10},
                }
            }
        )
    ]
)

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
