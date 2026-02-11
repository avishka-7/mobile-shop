import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stock Status", layout="wide")

st.title("Inventory & Stock Intelligence")

# ---------------- LOAD DATA ----------------
sales_df = pd.read_csv("mobile_sales.csv")
inventory_df = pd.read_csv("inventory.csv")

sales_df.columns = sales_df.columns.str.strip()
inventory_df.columns = inventory_df.columns.str.strip()

# ---------------- CLEAN DATE ----------------
sales_df["Date"] = pd.to_datetime(
    sales_df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_df = sales_df.dropna(subset=["Date"])

# ---------------- CALCULATE UNITS SOLD ----------------
units_sold = (
    sales_df
    .groupby("Mobile_Model")
    .size()
    .reset_index(name="Units_Sold")
)

# Merge with inventory
stock_df = pd.merge(
    inventory_df,
    units_sold,
    on="Mobile_Model",
    how="left"
)

stock_df["Units_Sold"] = stock_df["Units_Sold"].fillna(0)
stock_df["Stock_Remaining"] = stock_df["Current_Stock"] - stock_df["Units_Sold"]

# ---------------- STOCK STATUS LOGIC ----------------
def stock_status(row):
    if row["Stock_Remaining"] <= 5:
        return "🔴 Low"
    elif row["Stock_Remaining"] <= 15:
        return "🟡 Moderate"
    else:
        return "🟢 Sufficient"

stock_df["Status"] = stock_df.apply(stock_status, axis=1)

# ---------------- KPIs ----------------
st.markdown("Stock Overview")

col1, col2, col3 = st.columns(3)

total_models = len(stock_df)
low_stock_models = len(stock_df[stock_df["Status"] == "🔴 Low"])
total_stock_value = stock_df["Stock_Remaining"].sum()

with col1:
    st.metric("Total Models", total_models)

with col2:
    st.metric("Low Stock Alerts", low_stock_models)

with col3:
    st.metric("Total Units Remaining", int(total_stock_value))

st.markdown("---")

# ---------------- CHARTS ----------------
colA, colB = st.columns(2)

# ---- Stock Remaining Chart ----
with colA:
    fig_stock = px.bar(
        stock_df,
        x="Stock_Remaining",
        y="Mobile_Model",
        orientation="h",
        color="Status",
        title="Stock Remaining by Model"
    )

    fig_stock.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig_stock, use_container_width=True)

# ---- Stock Status Distribution ----
with colB:

    comparison_df = stock_df[["Mobile_Model", "Units_Sold", "Stock_Remaining"]]

    fig_compare = px.bar(
        comparison_df,
        x="Mobile_Model",
        y=["Units_Sold", "Stock_Remaining"],
        barmode="group",
        title="Sales vs Remaining Stock Comparison"
    )

    fig_compare.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Mobile Model",
        yaxis_title="Units"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

# ---------------- TABLE ----------------
st.markdown("Detailed Stock Table")

st.dataframe(stock_df.sort_values("Stock_Remaining"))


