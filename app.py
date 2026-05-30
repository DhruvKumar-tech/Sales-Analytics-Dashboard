# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Generation Pipeline (Cached) ---
@st.cache_data
def generate_mock_sales_data():
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(120)]
    
    products = ['Cloud Enterprise AI', 'Data Pipeline API', 'MLOps Server Pro', 'Automated Reporting Engine']
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America']
    
    data = []
    for date in date_list:
        for _ in range(np.random.randint(3, 8)):
            product = np.random.choice(products)
            region = np.random.choice(regions)
            units = int(np.random.randint(1, 5))
            
            price_map = {'Cloud Enterprise AI': 1200, 'Data Pipeline API': 450, 'MLOps Server Pro': 850, 'Automated Reporting Engine': 300}
            unit_price = price_map[product]
            revenue = units * unit_price
            
            data.append([date, product, region, units, unit_price, revenue])
            
    df = pd.DataFrame(data, columns=['Date', 'Product', 'Region', 'Units', 'Unit_Price', 'Revenue'])
    return df

df_sales = generate_mock_sales_data()

# --- Sidebar Controls ---
st.sidebar.header("Filter Controls")

# --- Collapsible Quick Insights Guide ---
with st.sidebar.expander("ℹ️ Quick Analytics Tours", expanded=False):
    st.info(
        "To test the system dynamics like a senior stakeholder, try these combinations:\n\n"
        "1️⃣ **The Enterprise Deep Dive**:\n"
        "• Region: *North America*\n"
        "• Product: *Cloud Enterprise AI*\n"
        "*(See how it isolates top tier software sales margins)*\n\n"
        "2️⃣ **Emerging Markets Audit**:\n"
        "• Region: *Asia-Pacific* & *Latin America*\n"
        "• Product: *Select All*\n"
        "*(Check localized volume thresholds vs AOV deviations)*"
)

st.sidebar.markdown("---")

selected_region = st.sidebar.multiselect(
    "Select Sales Region:",
    options=df_sales['Region'].unique(),
    default=df_sales['Region'].unique()
)

selected_product = st.sidebar.multiselect(
    "Select Product Segment:",
    options=df_sales['Product'].unique(),
    default=df_sales['Product'].unique()
)


# --- Filter Application ---
filtered_df = df_sales[
    (df_sales['Region'].isin(selected_region)) & 
    (df_sales['Product'].isin(selected_product))
]

# --- Main Layout Title ---
st.title("Enterprise Sales Analytics Dashboard")
st.markdown("Interactive performance reporting tracking operational revenue trends and product distribution metrics.")
st.markdown("---")

# --- Executive KPI Summary Ribbon ---
total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Units'].sum()
avg_transaction = filtered_df['Revenue'].mean() if not filtered_df.empty else 0

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(label="Gross Revenue", value=f"${total_revenue:,.2f}")

with kpi_col2:
    st.metric(label="Volume Sold", value=f"{total_units:,} Units")

with kpi_col3:
    st.metric(label="Average Order Value (AOV)", value=f"${avg_transaction:,.2f}")

st.markdown("---")

# --- Analytics Visualization Layout Grid ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue Over Time")
    daily_sales = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
    fig_trend = px.line(daily_sales, x='Date', y='Revenue', template="plotly_dark")
    fig_trend.update_traces(line_color='#6366f1')
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("Revenue Share By Product")
    product_sales = filtered_df.groupby('Product')['Revenue'].sum().reset_index()
    fig_pie = px.pie(product_sales, values='Revenue', names='Product', hole=0.4, template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- Raw Data Ledger ---
with st.expander("View Filtered Operational Data"):
    st.dataframe(filtered_df.sort_values(by='Date', ascending=False), use_container_width=True)
