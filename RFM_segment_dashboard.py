#%%
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
import plotly.graph_objects as go
import squarify

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

recency=pd.DataFrame(ord_final.groupby('product_id')['order_purchase_timestamp'].max().reset_index())
recency['recent_days']=(recency['order_purchase_timestamp'].max()-recency['order_purchase_timestamp']).dt.days
frequency=pd.DataFrame(ord_final.groupby('product_id')['customer_id'].count().reset_index())
monetary=pd.DataFrame(ord_final[['product_id','payment_value']].groupby('product_id')['payment_value'].sum().reset_index())

#now I will merge recency,frequency and monetary dataframe
df_rfm=pd.merge(recency,frequency,on='product_id')
df_rfm=pd.merge(df_rfm,monetary,on='product_id')

df_rfm=pd.merge(recency,frequency,on='product_id')
df_rfm=pd.merge(df_rfm,monetary,on='product_id')

df_rfm.drop(['order_purchase_timestamp'],axis=1,inplace=True)

df_rfm.columns=['product_id','Recency','Frequency','Monetary']
df_rfm.reset_index()
df_rfm.set_index("product_id",inplace=True)
    
quantiles=df_rfm.quantile(q=[0.25,0.5,0.75])
quantiles.to_dict()

#x=value, p=recency,frequency, monetary_value,  d=quartiles dict
def RScore(x,p,d):
    if x<=d[p][0.25]:
        return 4
    elif x<= d[p][0.50]:
        return 3
    elif x<= d[p][0.75]:
        return 2
    else:
        return 1

# x=value, p=recency,frequency, monetary_value,  k=quartiles dict
def FMScore(x,p,k):
    if x<=k[p][0.25]:
        return 1
    elif x<=k[p][0.50]:
        return 2
    elif x<=k[p][0.75]:
        return 3
    else:
        return 4

#create RFM segmentation table
rfm_segmentation=df_rfm
rfm_segmentation['R_Quartile']=rfm_segmentation["Recency"].apply(RScore,args=('Recency',quantiles))
rfm_segmentation['F_Quartile']=rfm_segmentation["Frequency"].apply(FMScore,args=('Frequency',quantiles))
rfm_segmentation['M_Quartile']=rfm_segmentation["Monetary"].apply(FMScore,args=('Monetary',quantiles))

rfm_segmentation['RFMScore']=rfm_segmentation.R_Quartile.map(str)+rfm_segmentation.F_Quartile.map(str)+rfm_segmentation.M_Quartile.map(str)

def segment(x):
    if x in ['444','443','433','442','434']:
        return 'Best_customer'
    elif x in [ '432','341','342','332','333','344','343','441']:
        return 'Loyal_customer'
    elif x in ['334', '234','214','224','413','314','244','243']:
        return 'Big_spender'
    elif x in ['212', '213', '222','211','114','311','312','214','143','142','141','241']:
        return 'Almost_lost'
    elif x in ['111', '121','112','113','144']:
        return 'Lost_customer'
    else:
        return 'New_customer'

rfm_segmentation['segments'] = rfm_segmentation['RFMScore'].apply(segment)

segmentwise = rfm_segmentation.groupby('segments').agg(RecencyMean = ('Recency', 'mean'),
                                          FrequencyMean = ('Frequency', 'mean'),
                                          MonetaryMean = ('Monetary', 'mean'),
                                          GroupSize = ('Recency', 'size'))

# Creating the Dash application
app = dash.Dash(__name__)

# Defining the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("RFM Segments"),
        dcc.Graph(
            id="rfm-segments-graph",
            figure={
                'data': [
                    go.Bar(
                        x=segmentwise.index,
                        y=segmentwise['GroupSize'],
                        marker={'color': ['yellow', 'limegreen', 'orange', 'red', 'blue', 'coral']}
                    )
                ],
                'layout': {
                    'title': 'RFM Segments',
                    'xaxis': {'title': 'Segments'},
                    'yaxis': {'title': 'Group Size'},
                }
            }
        )
    ]
)

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)