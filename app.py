import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 🎨 ستايل احترافي
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: #f8fafc;
}

[data-testid="stMetric"] {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}

[data-testid="stFileUploader"] {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# 📌 Sidebar
st.sidebar.title("📊 Sales Dashboard")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 🧠 نحول التاريخ
    df["Date"] = pd.to_datetime(df["Date"])

    # 🔎 فلترة المنتجات
    st.sidebar.subheader("🔎 Filters")

    products = df["Product"].unique()
    selected_product = st.sidebar.multiselect(
        "Select Product",
        products,
        default=products
    )

    df = df[df["Product"].isin(selected_product)]

    # 📅 فلترة التاريخ
    date_range = st.sidebar.date_input("Select Date Range", [])

    if len(date_range) == 2:
        df = df[
            (df["Date"] >= pd.to_datetime(date_range[0])) &
            (df["Date"] <= pd.to_datetime(date_range[1]))
        ]
# 🧠 لو مفيش ملف
if not uploaded_file:
    st.markdown("""
    <div style='text-align:center; padding:80px; color:#94a3b8'>
        <h2>📂 Upload your CSV file to start</h2>
    </div>
    """, unsafe_allow_html=True)

else:

    st.title("📈 Sales Dashboard")

    # 🧮 Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", df["Sales"].sum())
    col2.metric("📦 Orders", len(df))
    col3.metric("📊 Avg Sales", round(df["Sales"].mean(), 2))

    # 📊 Charts
    col4, col5 = st.columns(2)

    with col4:
        fig = px.line(df, x="Date", y="Sales", title="Sales Over Time")
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        fig2 = px.bar(df, x="Product", y="Sales", title="Sales by Product")
        st.plotly_chart(fig2, use_container_width=True)

    # 📋 Table
    st.subheader("📄 Data Preview")
    st.dataframe(df, use_container_width=True)
