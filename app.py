import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Dashboard")

st.write("ارفع ملف CSV وشوف التحليل 👇")

uploaded_file = st.file_uploader("اختار ملف CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 البيانات")
    st.dataframe(df)

    st.subheader("📈 إحصائيات")
    st.write(df.describe())

    st.subheader("📊 الرسم البياني")
    numeric_cols = df.select_dtypes(include='number')

    if not numeric_cols.empty:
        st.bar_chart(numeric_cols)
    else:
        st.warning("مفيش أعمدة رقمية للرسم")
