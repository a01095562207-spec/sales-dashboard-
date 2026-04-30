import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
# =========================
# 🚀 Page Config
# =========================
st.set_page_config(
    page_title="Advanced Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# 🎨 Custom CSS
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: white;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1, h2, h3, h4 {
    color: #f8fafc;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e293b;
}

[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.85);
    border: 2px dashed #38bdf8;
    padding: 20px;
    border-radius: 18px;
}

.stButton>button {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: white;
    border: none;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

.custom-box {
    background: rgba(30, 41, 59, 0.85);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 📌 Sidebar
# =========================
st.sidebar.title("📊 Sales Dashboard")
st.sidebar.subheader("🤖 Ask Your Data")

user_question = st.sidebar.text_input("Ask a question about sales")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================
# 📂 Empty State
# =========================
if not uploaded_file:

    st.markdown("""
    <div style='text-align:center; padding-top:120px'>
        <h1>📊 Advanced Sales Dashboard</h1>
        <p style='font-size:20px; color:#94a3b8'>
            Upload your CSV file to begin analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 📈 Main Dashboard
# =========================
else:

    # =========================
    # ⏳ Load CSV
    # =========================
    with st.spinner("Loading data..."):

        try:
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error("❌ CSV file is empty.")
                st.stop()

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            st.stop()

    # =========================
    # 🧹 Data Validation
    # =========================
    required_columns = ["Date", "Product", "Sales"]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            f"❌ Missing columns: {', '.join(missing_columns)}"
        )
        st.stop()

    # =========================
    # 🧠 Data Cleaning
    # =========================
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna()

    # =========================
    # 🔎 Filters
    # =========================
    st.sidebar.subheader("🔎 Filters")

    products = sorted(df["Product"].unique())

    selected_products = st.sidebar.multiselect(
        "Select Product",
        products,
        default=products
    )

    filtered_df = df[
        df["Product"].isin(selected_products)
    ]

    # =========================
    # 📅 Date Filter
    # =========================
    min_date = df["Date"].min()
    max_date = df["Date"].max()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    if len(selected_dates) == 2:

        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])

        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) &
            (filtered_df["Date"] <= end_date)
        ]

    # =========================
    # 📈 Title
    # =========================
    st.title("📈 Advanced Sales Dashboard")

    st.markdown("""
    <div class='custom-box'>
        Analyze your sales performance with AI-powered insights 🚀
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 💎 KPI Cards
    # =========================
    total_sales = filtered_df["Sales"].sum()
    avg_sales = filtered_df["Sales"].mean()
    total_orders = len(filtered_df)

    top_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

    col2.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "📊 Average Sale",
        f"${avg_sales:,.0f}"
    )

    col4.metric(
        "🏆 Top Product",
        top_product
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # 🤖 AI Insights
    # =========================
    st.subheader("🤖 AI Insights")

    top_sales = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .max()
    )

    best_day = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .idxmax()
    )

    best_day_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .max()
    )

    st.success(
        f"""
🔥 Top Product: {top_product}

💰 Total Sales for {top_product}: ${top_sales:,.0f}

📅 Best Sales Day: {best_day.date()}

🚀 Sales on Best Day: ${best_day_sales:,.0f}

📊 Average Sale Value: ${avg_sales:,.0f}
"""
    )

    # =========================
    # 📊 Charts
    # =========================
    chart1, chart2 = st.columns(2)

    with chart1:

        sales_over_time = (
            filtered_df.groupby("Date")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            sales_over_time,
            x="Date",
            y="Sales",
            title="📈 Sales Over Time",
            markers=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:

        sales_by_product = (
            filtered_df.groupby("Product")["Sales"]
            .sum()
            .reset_index()
        )

        fig2 = px.bar(
            sales_by_product,
            x="Product",
            y="Sales",
            title="📦 Sales by Product",
            text_auto=True
        )

        fig2.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =========================
    # 🥧 Pie Chart
    # =========================
    st.subheader("🥧 Sales Distribution")

    fig3 = px.pie(
        sales_by_product,
        names="Product",
        values="Sales",
        hole=0.5
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
    # =========================
    # 🤖 Sales Forecast
    # =========================

    st.subheader("📈 AI Sales Forecast")

    # تجهيز البيانات
    forecast_df = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
    )

    # تحويل التاريخ لأرقام
    forecast_df["Days"] = np.arange(len(forecast_df))

    X = forecast_df[["Days"]]
    y = forecast_df["Sales"]

    # تدريب الموديل
    model = LinearRegression()
    model.fit(X, y)

    # توقع 7 أيام جاية
    future_days = np.arange(
        len(forecast_df),
        len(forecast_df) + 7
    ).reshape(-1, 1)

    predictions = model.predict(future_days)

    # تجهيز الداتا الجديدة
    future_dates = pd.date_range(
        start=forecast_df["Date"].max(),
        periods=8,
        freq="D"
    )[1:]

    future_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Sales": predictions
    })

    # رسم التوقعات
    fig4 = px.line(
        future_df,
        x="Date",
        y="Predicted Sales",
        title="🔮 Next 7 Days Sales Prediction",
        markers=True
    )

    fig4.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )
    # =========================
    # 📋 Data Preview
    # =========================
    st.subheader("📄 Data Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )

    # =========================
    # 📥 Download CSV
    # =========================
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )
# =========================
# 🤖 Simple Data Chat
# =========================

if user_question:

    # 📊 نحول جزء من الداتا لنص
    sample_data = filtered_df.head(20).to_string(index=False)

    prompt = f"""
أنت محلل بيانات محترف.

هذه بيانات المبيعات:
{sample_data}

السؤال:
{user_question}

جاوب بشكل بسيط وواضح وبالعربي.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت محلل بيانات محترف."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        st.success("🤖 AI Answer")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ AI Error: {e}")
