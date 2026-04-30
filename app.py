import streamlit as st
import pandas as pd
import plotly.express as px

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

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Titles */
h1, h2, h3, h4 {
    color: #f8fafc;
    font-weight: 700;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e293b;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.85);
    border: 2px dashed #38bdf8;
    padding: 20px;
    border-radius: 18px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #38bdf8, #6366f1);
    color: white;
    border: none;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    opacity: 0.9;
}

/* Success box */
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

    # ⏳ Loading
    with st.spinner("Loading data..."):
        df = pd.read_csv(uploaded_file)

    # =========================
    # 🧹 Data Cleaning
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

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Remove nulls
    df = df.dropna()

    # =========================
    # 🔎 Sidebar Filters
    # =========================
    st.sidebar.subheader("🔎 Filters")

    # Product Filter
    products = sorted(df["Product"].unique())

    selected_products = st.sidebar.multiselect(
        "Select Product",
        products,
        default=products
    )

    # Date Filter
    min_date = df["Date"].min()
    max_date = df["Date"].max()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    # Apply Filters
    filtered_df = df[
        df["Product"].isin(selected_products)
    ]

    if len(selected_dates) == 2:
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])

        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) &
            (filtered_df["Date"] <= end_date)
        ]

    # =========================
    # 📈 Dashboard Title
    # =========================
    st.title("📈 Advanced Sales Dashboard")

    st.markdown("""
    <div class='custom-box'>
        Analyze your sales performance with interactive charts and KPIs 🚀
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
    # 📊 Charts Row 1
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
