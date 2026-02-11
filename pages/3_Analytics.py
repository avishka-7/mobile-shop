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

# -------- AUTO GENERATE BRAND COLUMN --------
def extract_brand(model):
    if "Samsung" in model:
        return "Samsung"
    elif "iPhone" in model:
        return "Apple"
    elif "Redmi" in model:
        return "Redmi"
    elif "Realme" in model:
        return "Realme"
    elif "OnePlus" in model:
        return "OnePlus"
    elif "Vivo" in model:
        return "Vivo"
    elif "Oppo" in model:
        return "Oppo"
    else:
        return "Other"

sales_df["Brand"] = sales_df["Mobile_Model"].apply(extract_brand)


# ---------------- BRAND FILTER ----------------
st.sidebar.header("Filter")

brands = sales_df["Brand"].unique().tolist()
brand_options = ["All Brands"] + brands

selected_brand = st.sidebar.selectbox(
    "Select Brand",
    brand_options
)

# Apply Filter
if selected_brand == "All Brands":
    filtered_df = sales_df
else:
    filtered_df = sales_df[sales_df["Brand"] == selected_brand]

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

st.markdown("---")

# ---------------- OVERALL DASHBOARD ----------------
if selected_brand == "All Brands":

    st.markdown("Overall Business Performance")

    # Brand Revenue Comparison
    brand_revenue = (
        sales_df
        .groupby("Brand")["Price"]
        .sum()
        .reset_index()
    )

    fig_brand = px.bar(
        brand_revenue,
        x="Brand",
        y="Price",
        title="Revenue by Brand",
        color="Brand"
    )

    fig_brand.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(fig_brand, use_container_width=True)

    # Overall Monthly Trend
    monthly_units = (
        sales_df
        .groupby(sales_df["Date"].dt.to_period("M"))
        .size()
        .reset_index(name="Units")
    )

    monthly_units["Date"] = monthly_units["Date"].astype(str)

    fig_month = px.line(
        monthly_units,
        x="Date",
        y="Units",
        markers=True,
        title="Overall Monthly Sales Trend"
    )

    fig_month.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(fig_month, use_container_width=True)

    st.stop()  # IMPORTANT: stops brand-specific charts below

# ---------------- CHARTS ----------------
st.markdown("Brand Performance")

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
            title=f"{selected_brand} Monthly Sales Trend"
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
            title=f"{selected_brand} Revenue by Model"
        )
def format_indian(value):
    if value >= 10000000:
        return f"₹ {value/10000000:.1f}Cr"
    elif value >= 100000:
        return f"₹ {value/100000:.1f}L"
    elif value >= 1000:
        return f"₹ {value/1000:.1f}K"
    else:
        return f"₹ {value}"

        fig2.update_layout(
            template="plotly_dark",
            height=350,
            xaxis=dict(
                tickvals=revenue_model["Price"],
                ticktext=[format_indian(val) for val in revenue_model["Price"]]
            )
        )


        st.plotly_chart(fig2, use_container_width=True)

# ---- Units Distribution ----
st.markdown("###Model Distribution")

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
        title=f"{selected_brand} Units Share"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(fig3, use_container_width=True)


