import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Read the datasets
all_df = pd.read_csv("C:/Users/ASUS/Downloads/E-Commerce Public/all_data.csv")
df_products = pd.read_csv("C:/Users/ASUS/Downloads/E-Commerce Public/df_products.csv")
customers_df = pd.read_csv("C:/Users/ASUS/Downloads/E-Commerce Public/customers_df.csv")

def create_rfm_df(all_df):
    all_df['total_price'] = all_df['price'] + all_df['freight_value']
    rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",  # mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"])
    all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])
    recent_date = all_df["order_purchase_timestamp"].max().date()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].dt.date.apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

# Call the function to create rfm_df
rfm_df = create_rfm_df(all_df)

st.header('Simple Dashboard E-Commerce')

# Additional Visualization 1
st.subheader('Top 5 Order by Product Category')

# Calculate top 5 product categories
product_category = df_products.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head()

# Create a new figure for the plot
fig2, ax2 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:5]

product_category.plot(kind='bar', color=colors, ax=ax2)
ax2.set_title('Top 5 Order by Product Category', fontsize=20)
ax2.set_xlabel('Product Category', fontsize=15)
ax2.set_ylabel('Count', fontsize=15)
ax2.tick_params(axis='x', rotation=45, labelsize=12)
ax2.tick_params(axis='y', labelsize=12)
plt.tight_layout()

st.pyplot(fig2)

# Additional Visualization 2
st.subheader('Top Payment Type')

# Calculate payment type counts
payment_type = customers_df['payment_type'].value_counts()

# Create a new figure for the plot
fig3, ax3 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:len(payment_type)]

payment_type.plot(kind='bar', color=colors, ax=ax3)
ax3.set_title('Top Payment Type', fontsize=20)
ax3.set_xlabel('Payment Type', fontsize=15)
ax3.set_ylabel('Count', fontsize=15)
ax3.tick_params(axis='x', rotation=0, labelsize=12)
ax3.tick_params(axis='y', labelsize=12)
plt.tight_layout()

st.pyplot(fig3)

# Additional Visualization 3
st.subheader('Top Delivered Status')

# Calculate delivery status counts
delivers_customer = customers_df['order_status'].value_counts()

# Create a new figure for the plot
fig4, ax4 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:len(delivers_customer)]

delivers_customer.plot(kind='bar', color=colors, ax=ax4)
ax4.set_title('Top Delivered Status', fontsize=20)
ax4.set_xlabel('Delivered Status', fontsize=15)
ax4.set_ylabel('Count', fontsize=15)
ax4.tick_params(axis='x', rotation=0, labelsize=12)
ax4.tick_params(axis='y', labelsize=12)
plt.tight_layout()

st.pyplot(fig4)

# Moved Visualization: Top 5 Customer States
st.subheader('Top 5 Customer States')

# Calculate the top 5 customer states
top_states = customers_df['customer_state'].value_counts().head()

# Create a new figure for the plot
fig5, ax5 = plt.subplots(figsize=(12, 8))
colors = sns.color_palette('pastel')[0:len(top_states)]

top_states.plot(kind='bar', color=colors, ax=ax5)
ax5.set_title('Top 5 Customer States', fontsize=20)
ax5.set_xlabel('Customer State', fontsize=15)
ax5.set_ylabel('Count', fontsize=15)
ax5.tick_params(axis='x', rotation=0, labelsize=12)
ax5.tick_params(axis='y', labelsize=12)
plt.tight_layout()

st.pyplot(fig5)

# Moved to Bottom: Best Customer Based on RFM Parameters
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
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
