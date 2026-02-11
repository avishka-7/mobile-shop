import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics", layout="wide")

st.title("Sales Overview")

# ---------------- LOAD DATA ----------------
sales_df = pd.read_csv("mobile_sales.csv")
sales_df.columns = sales_df.columns.str.strip()

sales_df["Date"] = pd.to_datetime(
    sales_df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_df = sales_df.dropna(subset=["Date"])

# ---------------- KPI SECTION ----------------
st.markdown("## 📊 Overview")

total_revenue = sales_df["Price"].sum()
total_sales = len(sales_df)
avg_sale = sales_df["Price"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"₹{int(total_revenue):,}")
col2.metric("Sales", total_sales)
col3.metric("Average Sale", f"₹{int(avg_sale):,}")

# ---- Monthly Sales Trend ----
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Monthly Sales")

    monthly_units = (
        sales_df
        .groupby(sales_df["Date"].dt.to_period("M"))
        .size()
    )

    monthly_units.index = monthly_units.index.astype(str)

    fig1, ax1 = plt.subplots(figsize=(4,3))
    ax1.plot(monthly_units.index, monthly_units.values, marker="o")
    ax1.set_xticklabels(monthly_units.index, rotation=45)
    ax1.set_ylabel("Units")
    ax1.set_xlabel("Month")
    fig1.tight_layout()

    st.pyplot(fig1)

# ---- Revenue by Model ----
with col2:
    st.markdown("### 💰 Revenue by Model")

    model_revenue = (
        sales_df
        .groupby("Mobile_Model")["Price"]
        .sum()
        .sort_values()
    )

    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.barh(model_revenue.index, model_revenue.values)
    ax2.set_xlabel("Revenue")
    fig2.tight_layout()

    st.pyplot(fig2)

# ---- Units Share Donut ----
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🔵 Units Share")

    units_sold = sales_df["Mobile_Model"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(4,3))
    wedges, texts, autotexts = ax3.pie(
        units_sold,
        autopct="%1.1f%%",
        startangle=90
    )

    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    fig3.gca().add_artist(centre_circle)

    ax3.legend(
        wedges,
        units_sold.index,
        title="Models",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    fig3.tight_layout()
    st.pyplot(fig3)

with col4:
    st.markdown("### 📊 Units Sold Table")
    st.dataframe(units_sold.reset_index().rename(
        columns={"index": "Mobile Model", "Mobile_Model": "Units Sold"}
    ))
