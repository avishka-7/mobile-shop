import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics", layout="wide")

st.title("Sales Analytics & Demand Prediction")

# ---------- LOAD DATA ----------
sales_df = pd.read_csv("mobile_sales.csv")
sales_df.columns = sales_df.columns.str.strip()

sales_df["Date"] = pd.to_datetime(
    sales_df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_df = sales_df.dropna(subset=["Date"])

# ---------- KPIs ----------
st.subheader("Key Metrics")

col1, col2 = st.columns(2)

total_revenue = sales_df["Price"].sum()
total_units = len(sales_df)

col1.metric("💰 Total Revenue", f"₹{int(total_revenue)}")
col2.metric("📦 Total Units Sold", total_units)

st.markdown("---")

# ---------- SALES TREND ----------
st.subheader("Sales Trend")

monthly_sales = (
    sales_df
    .groupby(sales_df["Date"].dt.to_period("M"))
    .size()
)

monthly_sales.index = monthly_sales.index.astype(str)

fig, ax = plt.subplots()
monthly_sales.plot(kind="line", marker="o", ax=ax)
ax.set_ylabel("Units Sold")
ax.set_xlabel("Month")

st.pyplot(fig)

st.markdown("---")

# ---------- SALES BY MODEL ----------
st.subheader("Sales by Mobile Model")

model_sales = sales_df["Mobile_Model"].value_counts()

fig2, ax2 = plt.subplots()
model_sales.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Units Sold")

st.pyplot(fig2)

st.markdown("---")

# ---------- HYBRID DEMAND PREDICTION ----------
st.subheader("Next Month Demand Prediction")

prediction_results = []

# Add Month column
sales_df["Month"] = sales_df["Date"].dt.to_period("M")

for model in sales_df["Mobile_Model"].unique():

    model_data = sales_df[sales_df["Mobile_Model"] == model]

    monthly_model_sales = (
        model_data
        .groupby("Month")
        .size()
    )

    if len(monthly_model_sales) >= 2:

        average_sales = monthly_model_sales.mean()

        last_month = monthly_model_sales.iloc[-1]
        prev_month = monthly_model_sales.iloc[-2]

        trend = last_month - prev_month

        predicted = (0.7 * average_sales) + (0.3 * trend)

        predicted = max(round(predicted), 0)

        suggested_stock = round(predicted * 1.1)

        prediction_results.append([
            model,
            round(average_sales, 1),
            trend,
            predicted,
            suggested_stock
        ])

# Create dataframe
prediction_df = pd.DataFrame(
    prediction_results,
    columns=[
        "Mobile_Model",
        "Avg Monthly Sales",
        "Recent Trend",
        "Predicted Next Month",
        "Suggested Stock"
    ]
)

st.dataframe(prediction_df)

