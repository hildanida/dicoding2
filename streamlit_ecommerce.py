import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Read the datasets
all_df = pd.read_csv("all_data.csv")
df_products = pd.read_csv("df_products.csv")
customers_df = pd.read_csv("customers_df.csv")

# Convert order_purchase_timestamp to datetime
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# Sidebar untuk filter tanggal
st.sidebar.header("Filter by Date")
start_date = st.sidebar.date_input("Start Date", all_df["order_purchase_timestamp"].min().date())
end_date = st.sidebar.date_input("End Date", all_df["order_purchase_timestamp"].max().date())

# Filter data berdasarkan rentang tanggal
filtered_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) &
                      (all_df["order_purchase_timestamp"].dt.date <= end_date)]

def create_rfm_df(df):
    df['total_price'] = df['price'] + df['freight_value']
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"])
    recent_date = df["order_purchase_timestamp"].max().date()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].dt.date.apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

# Create RFM DataFrame
rfm_df = create_rfm_df(filtered_df)

st.header('Simple Dashboard E-Commerce')

# Visualization: Top 5 Order by Product Category
st.subheader('Top 5 Order by Product Category')
product_category = df_products.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head()
fig2, ax2 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:5]
product_category.plot(kind='bar', color=colors, ax=ax2)
ax2.set_title('Top 5 Order by Product Category', fontsize=20)
st.pyplot(fig2)

# Visualization: Top Payment Type
st.subheader('Top Payment Type')
payment_type = customers_df['payment_type'].value_counts()
fig3, ax3 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:len(payment_type)]
payment_type.plot(kind='bar', color=colors, ax=ax3)
st.pyplot(fig3)

# Visualization: Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "R$", locale='es_CO')
    st.metric("Average Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9"] * 5
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
st.pyplot(fig)
