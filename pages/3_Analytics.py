import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics", layout="wide")

st.title("Sales Analytics Dashboard")

# ---------------- LOAD DATA ----------------
sales_df = pd.read_csv("mobile_sales.csv")
sales_df.columns = sales_df.columns.str.strip()

sales_df["Date"] = pd.to_datetime(
    sales_df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_df = sales_df.dropna(subset=["Date"])

# ---------------- FILTERS ----------------
st.sidebar.header("🔎 Filters")

# Model Filter
models = sales_df["Mobile_Model"].unique()
selected_models = st.sidebar.multiselect(
    "Select Model(s)",
    models,
    default=models
)

# Date Range Filter
min_date = sales_df["Date"].min()
max_date = sales_df["Date"].max()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Apply Filters
filtered_df = sales_df[
    (sales_df["Mobile_Model"].isin(selected_models)) &
    (sales_df["Date"] >= pd.to_datetime(selected_dates[0])) &
    (sales_df["Date"] <= pd.to_datetime(selected_dates[1]))
]

# ---------------- KPIs ----------------
st.markdown("## Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", len(filtered_df))

with col2:
    st.metric("Total Revenue", f"₹ {filtered_df['Price'].sum():,.0f}")

with col3:
    if len(filtered_df) > 0:
        st.metric("Avg Sale Value", f"₹ {filtered_df['Price'].mean():,.0f}")
    else:
        st.metric("Avg Sale Value", "₹ 0")

# ---------------- CHARTS ----------------
st.markdown("---")
st.markdown("## Sales Insights")

colA, colB = st.columns(2)

# ---- Monthly Trend ----
with colA:
    monthly_units = (
        filtered_df
        .groupby(filtered_df["Date"].dt.to_period("M"))
        .size()
        .reset_index(name="Units")
    )

    if not monthly_units.empty:
        monthly_units["Date"] = monthly_units["Date"].astype(str)

        fig1 = px.line(
            monthly_units,
            x="Date",
            y="Units",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig1.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig1, use_container_width=True)

# ---- Revenue by Model ----
with colB:
    revenue_model = (
        filtered_df
        .groupby("Mobile_Model")["Price"]
        .sum()
        .reset_index()
    )

    if not revenue_model.empty:
        fig2 = px.bar(
            revenue_model,
            x="Price",
            y="Mobile_Model",
            orientation="h",
            title="Revenue by Model"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---- Units Share Donut ----
st.markdown("### Units Sold Distribution")

units_share = (
    filtered_df["Mobile_Model"]
    .value_counts()
    .reset_index()
)

if not units_share.empty:
    units_share.columns = ["Mobile_Model", "Units"]

    fig3 = px.pie(
        units_share,
        values="Units",
        names="Mobile_Model",
        hole=0.6,
        title="Units Share"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(fig3, use_container_width=True)

