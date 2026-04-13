import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Data Dashboard")
st.markdown("### تحليل احترافي لبيانات المبيعات 👨‍💻")

# Upload
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar Filters 🔥
    st.sidebar.header("🎛️ Filters")

    region = st.sidebar.multiselect(
        "Select Region", options=df['Region'].unique(), default=df['Region'].unique()
    )

    product = st.sidebar.multiselect(
        "Select Product", options=df['Product'].unique(), default=df['Product'].unique()
    )

    # فلترة
    filtered_df = df[(df['Region'].isin(region)) & (df['Product'].isin(product))]

    # KPIs 💎
    total_sales = filtered_df['Sales'].sum()
    avg_sales = filtered_df['Sales'].mean()
    total_orders = len(filtered_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"{total_sales}")
    col2.metric("📊 Avg Sales", f"{avg_sales:.2f}")
    col3.metric("🧾 Orders", total_orders)

    st.markdown("---")

    # 📊 Plotly Charts
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            filtered_df.groupby('Product')['Sales'].sum().reset_index(),
            x='Product',
            y='Sales',
            color='Product',
            title="Top Products"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(
            filtered_df,
            names='Region',
            values='Sales',
            title="Sales by Region"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 📈 Trend
    st.subheader("📈 Sales Over Time")

    monthly = filtered_df.resample('M', on='Date')['Sales'].sum().reset_index()

    fig3 = px.line(
        monthly,
        x='Date',
        y='Sales',
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # 🤖 Prediction
    st.subheader("🤖 Sales Prediction")

    monthly['Month'] = monthly['Date'].dt.month

    X = monthly[['Month']]
    y = monthly['Sales']

    model = LinearRegression()
    model.fit(X, y)

    future = np.array([[13],[14],[15]])
    pred = model.predict(future)

    st.write("📊 Predicted Next 3 Months:", pred)

    # رسم التوقع
    fig4 = px.line(monthly, x='Month', y='Sales', title="Prediction Trend")
    st.plotly_chart(fig4, use_container_width=True)
