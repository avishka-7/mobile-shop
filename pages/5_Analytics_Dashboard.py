import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobile Sales Dashboard", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("mobile_sales.csv")
df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df = df.dropna(subset=["Date"])

# ---------- TITLE ----------
st.markdown("<h1 style='text-align: center;'>📊 Mobile Sales Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔎 Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

selected_models = st.sidebar.multiselect(
    "Select Mobile Models",
    df["Mobile_Model"].unique(),
    default=df["Mobile_Model"].unique()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Mobile_Model"].isin(selected_models))
]

# ---------- KPI CARDS ----------
total_revenue = filtered_df["Price"].sum()
total_units = len(filtered_df)
avg_price = filtered_df["Price"].mean()

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
    <div style="background-color:#1f77b4;padding:20px;border-radius:10px">
        <h3 style="color:white;">💰 Total Revenue</h3>
        <h2 style="color:white;">₹{int(total_revenue)}</h2>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style="background-color:#2ca02c;padding:20px;border-radius:10px">
        <h3 style="color:white;">📦 Units Sold</h3>
        <h2 style="color:white;">{total_units}</h2>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style="background-color:#ff7f0e;padding:20px;border-radius:10px">
        <h3 style="color:white;">📊 Avg Price</h3>
        <h2 style="color:white;">₹{int(avg_price)}</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- SALES TREND ----------
st.subheader("📈 Sales Trend Over Time")

daily_sales = filtered_df.groupby("Date").size().reset_index(name="Units")

fig_trend = px.line(
    daily_sales,
    x="Date",
    y="Units",
    markers=True,
    title="Daily Sales Trend"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ---------- PRODUCT PERFORMANCE ----------
col4, col5 = st.columns(2)

with col4:
    st.subheader("📱 Units Sold by Model")
    units_model = filtered_df["Mobile_Model"].value_counts().reset_index()
    units_model.columns = ["Mobile_Model", "Units"]

    fig_units = px.bar(
        units_model,
        x="Mobile_Model",
        y="Units",
        color="Units",
        title="Units Sold",
        text="Units"
    )
    st.plotly_chart(fig_units, use_container_width=True)

with col5:
    st.subheader("💰 Revenue by Model")
    revenue_model = filtered_df.groupby("Mobile_Model")["Price"].sum().reset_index()

    fig_revenue = px.pie(
        revenue_model,
        names="Mobile_Model",
        values="Price",
        title="Revenue Contribution"
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown("---")

# ---------- FAST VS SLOW MOVERS ----------
st.subheader("⚡ Fast vs Slow Movers")

avg_units = units_model["Units"].mean()

units_model["Category"] = units_model["Units"].apply(
    lambda x: "Fast Moving" if x >= avg_units else "Slow Moving"
)

fig_category = px.bar(
    units_model,
    x="Mobile_Model",
    y="Units",
    color="Category",
    title="Fast vs Slow Moving Models"
)

st.plotly_chart(fig_category, use_container_width=True)

# ---------- DATA TABLE ----------
with st.expander("📋 View Detailed Data"):
    st.dataframe(filtered_df)

