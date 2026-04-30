import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
import google.generativeai as genai
import os

# =========================
# 🤖 Gemini AI Setup
# =========================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# 🚀 Page Config
# =========================
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# 🎨 Simple UI Style
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

#MainMenu, footer, header {visibility: hidden;}

h1, h2, h3 {
    color: #f8fafc;
}

[data-testid="stMetric"] {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 📌 Sidebar
# =========================
st.sidebar.title("📊 Sales Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
user_question = st.sidebar.text_input("🤖 اسأل الداتا")

# =========================
# 📂 Empty State
# =========================
if not uploaded_file:
    st.title("📊 Sales Dashboard")
    st.info("ارفع ملف CSV للبدء 🚀")

else:

    # =========================
    # 📥 Load Data
    # =========================
    df = pd.read_csv(uploaded_file)

    if df.empty:
        st.error("❌ الملف فاضي")
        st.stop()

    required = ["Date", "Product", "Sales"]

    if any(col not in df.columns for col in required):
        st.error("❌ لازم الأعمدة: Date, Product, Sales")
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna()

    # =========================
    # 🔎 Filter
    # =========================
    products = df["Product"].unique()

    selected_products = st.sidebar.multiselect(
        "Select Product",
        products,
        default=products
    )

    filtered_df = df[df["Product"].isin(selected_products)]

    # =========================
    # 📊 Title
    # =========================
    st.title("📈 Sales Dashboard")

    # =========================
    # 💎 KPIs
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
    col2.metric("📦 Orders", len(filtered_df))
    col3.metric("📊 Avg", f"${filtered_df['Sales'].mean():,.0f}")
    col4.metric("🏆 Top Product",
                filtered_df.groupby("Product")["Sales"].sum().idxmax())

    # =========================
    # 📊 CHARTS (Simple Style)
    # =========================
    st.subheader("📊 Charts")

    chart1, chart2 = st.columns(2)

    sales_time = filtered_df.groupby("Date")["Sales"].sum().reset_index()

    with chart1:
        fig = px.line(
            sales_time,
            x="Date",
            y="Sales",
            title="📈 Sales Over Time",
            markers=True
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with chart2:
        prod_sales = filtered_df.groupby("Product")["Sales"].sum().reset_index()

        fig2 = px.bar(
            prod_sales,
            x="Product",
            y="Sales",
            title="📦 Sales by Product",
            text_auto=True
        )
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # 🥧 PIE CHART
    # =========================
    st.subheader("🥧 Sales Distribution")

    fig3 = px.pie(
        prod_sales,
        names="Product",
        values="Sales",
        hole=0.4
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # 🔮 FORECAST
    # =========================
    st.subheader("📈 AI Forecast")

    forecast_df = sales_time.copy()
    forecast_df["Days"] = np.arange(len(forecast_df))

    X = forecast_df[["Days"]]
    y = forecast_df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(len(forecast_df), len(forecast_df)+7).reshape(-1,1)
    preds = model.predict(future_days)

    future_dates = pd.date_range(
        start=forecast_df["Date"].max(),
        periods=8
    )[1:]

    future_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Sales": preds
    })

    fig4 = px.line(
        future_df,
        x="Date",
        y="Predicted Sales",
        title="🔮 Next 7 Days Forecast",
        markers=True
    )

    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

    # =========================
    # 🤖 AI CHAT (Gemini)
    # =========================
    if user_question:

        try:
            sample_data = filtered_df.head(30).to_string(index=False)

            prompt = f"""
أنت محلل بيانات محترف.

هذه بيانات المبيعات:
{sample_data}

السؤال:
{user_question}

جاوب بشكل بسيط وواضح بالعربي.
"""

            response = ai_model.generate_content(prompt)

            st.subheader("🤖 AI Answer")
            st.success(response.text)

        except Exception as e:
            st.error(f"❌ AI Error: {e}")

    # =========================
    # 📄 DATA
    # =========================
    st.subheader("📄 Data Preview")
    st.dataframe(filtered_df, use_container_width=True)
