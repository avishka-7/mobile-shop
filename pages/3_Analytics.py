import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics", layout="wide")

st.title("📊 Sales Analytics & Demand Prediction")

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

# ---------------- MONTHLY REVENUE AREA CHART ----------------
st.markdown("## 📈 Monthly Revenue Trend")

monthly_revenue = (
    sales_df
    .groupby(sales_df["Date"].dt.to_period("M"))["Price"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

st.area_chart(monthly_revenue)

st.markdown("---")

# ---------------- MODEL REVENUE BAR CHART ----------------
st.markdown("## 📱 Revenue by Mobile Model")

model_revenue = (
    sales_df
    .groupby("Mobile_Model")["Price"]
    .sum()
    .sort_values()
)

st.bar_chart(model_revenue)

st.markdown("---")

# ---------------- PAYMENT MODE PIE CHART ----------------
st.markdown("## 💳 Payment Distribution")

payment_counts = sales_df["Payment_Mode"].value_counts()

fig, ax = plt.subplots()
ax.pie(payment_counts, labels=payment_counts.index, autopct="%1.1f%%")
ax.set_title("Payment Mode Share")

st.pyplot(fig)

st.markdown("---")

# ---------------- DEMAND PREDICTION ----------------
st.markdown("## 🤖 AI-Based Demand Forecast")

sales_df["Month"] = sales_df["Date"].dt.to_period("M")

prediction_results = []

for model in sales_df["Mobile_Model"].unique():

    model_data = sales_df[sales_df["Mobile_Model"] == model]

    # Using monthly revenue for variation
    monthly_model_revenue = (
        model_data
        .groupby("Month")["Price"]
        .sum()
    )

    if len(monthly_model_revenue) >= 2:

        moving_avg = monthly_model_revenue.tail(3).mean()

        growth_rate = monthly_model_revenue.pct_change().mean()

        trend_forecast = monthly_model_revenue.iloc[-1] * (1 + growth_rate)

        hybrid_prediction = (0.6 * moving_avg) + (0.4 * trend_forecast)

        predicted = round(max(hybrid_prediction, 0))

        suggested_stock = round(predicted * 1.15)

        prediction_results.append([
            model,
            round(moving_avg, 2),
            round(growth_rate * 100, 2),
            predicted,
            suggested_stock
        ])

prediction_df = pd.DataFrame(
    prediction_results,
    columns=[
        "Mobile_Model",
        "Avg Monthly Revenue",
        "Growth Rate (%)",
        "Predicted Revenue Next Month",
        "Suggested Stock Level"
    ]
)

st.dataframe(prediction_df, use_container_width=True)
