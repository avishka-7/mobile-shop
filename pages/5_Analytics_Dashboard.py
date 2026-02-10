import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("mobile_sales.csv")
df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df = df.dropna(subset=["Date"])

st.title("📊 Mobile Sales Analytics Dashboard")

# ---------- SIDEBAR FILTER ----------
st.sidebar.header("Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

models = st.sidebar.multiselect(
    "Select Mobile Models",
    sorted(df["Mobile_Model"].unique()),
    default=sorted(df["Mobile_Model"].unique())
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Mobile_Model"].isin(models))
]

# ---------- KPIs ----------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"₹{int(filtered_df['Price'].sum())}")
col2.metric("📦 Units Sold", len(filtered_df))
col3.metric("📊 Avg Price", f"₹{int(filtered_df['Price'].mean())}")

st.markdown("---")

# ---------- SALES TREND ----------
st.subheader("📈 Sales Trend")

trend = filtered_df.groupby("Date").size()

fig1, ax1 = plt.subplots()
ax1.plot(trend.index, trend.values, marker="o")
ax1.set_xlabel("Date")
ax1.set_ylabel("Units Sold")
plt.xticks(rotation=45)

st.pyplot(fig1)

st.markdown("---")

# ---------- PRODUCT PERFORMANCE ----------
st.subheader("📱 Product Performance")

units_by_model = filtered_df["Mobile_Model"].value_counts()
revenue_by_model = filtered_df.groupby("Mobile_Model")["Price"].sum()

fig2, ax2 = plt.subplots()
units_by_model.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Units Sold")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig2)

fig3, ax3 = plt.subplots()
revenue_by_model.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Revenue (₹)")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig3)

st.markdown("---")

# ---------- FAST VS SLOW MOVERS ----------
st.subheader("⚡ Fast vs Slow Moving Products")

avg_sales = units_by_model.mean()

performance_df = pd.DataFrame({
    "Units Sold": units_by_model,
    "Category": ["Fast Moving" if x >= avg_sales else "Slow Moving" for x in units_by_model]
})

st.dataframe(performance_df)

# ---------- RAW DATA ----------
with st.expander("📋 View Filtered Data"):
    st.dataframe(filtered_df)
