import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Overview", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("mobile_sales.csv")

# Clean column names (removes hidden spaces)
df.columns = df.columns.str.strip()

# Check for date column safely
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
elif "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df.rename(columns={"date": "Date"}, inplace=True)
else:
    st.error("❌ Date column not found in dataset")
    st.stop()

st.title("📊 Sales Overview Dashboard")

# ---------- SIDEBAR FILTER ----------
st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max().date()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ---------- KPIs ----------
col1, col2, col3 = st.columns(3)

total_revenue = filtered_df["Price"].sum()
total_units = len(filtered_df)
avg_price = filtered_df["Price"].mean()

col1.metric("💰 Total Revenue", f"₹{int(total_revenue)}")
col2.metric("📦 Units Sold", total_units)
col3.metric("📊 Avg Selling Price", f"₹{int(avg_price)}")

st.markdown("---")

# ---------- SALES TREND ----------
st.subheader("📈 Sales Trend Over Time")

sales_by_date = (
    filtered_df
    .groupby("Date")
    .size()
    .reset_index(name="Sales_Count")
)

fig, ax = plt.subplots()
ax.plot(sales_by_date["Date"], sales_by_date["Sales_Count"], marker="o")
ax.set_xlabel("Date")
ax.set_ylabel("Units Sold")
ax.set_title("Daily Sales Trend")
plt.xticks(rotation=45)

st.pyplot(fig)

# ---------- DATA TABLE ----------
with st.expander("📋 View Filtered Sales Data"):
    st.dataframe(filtered_df)

