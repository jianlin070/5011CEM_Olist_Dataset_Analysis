import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px

orders = pd.read_csv("olist_orders_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
translations = pd.read_csv("product_category_name_translation.csv")

translations = translations.set_index('product_category_name')['product_category_name_english'].to_dict()
products['product_category_name'] = products['product_category_name'].map(translations)

order_products = pd.merge(items, products, left_on='product_id', right_on='product_id')

# drop the orders with missing category names
order_products = order_products.dropna(subset=["product_category_name", "order_id"])

order_products_dict = order_products[['product_category_name', 'order_id']] \
    .groupby('product_category_name')['order_id'] \
    .count() \
    .sort_values(ascending=False) \
    .to_dict()

order_product_names = list(order_products_dict.keys())[:20]
order_product_values = list(order_products_dict.values())[:20]

app = dash.Dash()

app.layout = html.Div(
    children=[
        dcc.Graph(
            figure=px.bar(
                order_products,
                x=order_product_names,
                y=order_product_values,
                text=order_product_values,
                title="Top 20 Product Categories by Orders",
                labels={'x': 'Category Name', 'y': 'Total orders'},
            ).update_traces(textposition='outside', cliponaxis=False)
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
