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

# ---------------- Monthly Sales Trend ----------------
st.markdown("## Monthly Sales Trend")

monthly_units = (
    sales_df
    .groupby(sales_df["Date"].dt.to_period("M"))
    .size()
)

monthly_units.index = monthly_units.index.astype(str)

st.line_chart(monthly_units)


# ---------------- MODEL REVENUE BAR CHART ----------------
st.markdown("## Revenue by Model")

import matplotlib.pyplot as plt

model_revenue = (
    sales_df
    .groupby("Mobile_Model")["Price"]
    .sum()
    .sort_values()
)

fig, ax = plt.subplots(facecolor="none")
ax.set_facecolor("none")

ax.barh(model_revenue.index, model_revenue.values)

ax.tick_params(colors="white")
ax.set_xlabel("Revenue", color="white")
ax.set_ylabel("Mobile Model", color="white")

st.pyplot(fig)


# ---------------- Units Sold Share ( Donut Chart) ----------------
st.markdown("## 🔵 Units Sold Share")

units_sold = sales_df["Mobile_Model"].value_counts()

fig2, ax2 = plt.subplots(facecolor="none")
ax2.set_facecolor("none")

wedges, texts, autotexts = ax2.pie(
    units_sold,
    labels=units_sold.index,
    autopct="%1.1f%%",
    startangle=90,
    textprops={"color": "white"}
)

centre_circle = plt.Circle((0, 0), 0.70, fc='black')
fig2.gca().add_artist(centre_circle)

st.pyplot(fig2)

# ---------------- DEMAND PREDICTION ----------------
st.markdown("## Next Month Sales Estimate")

sales_df["Month"] = sales_df["Date"].dt.to_period("M")

prediction_results = []

for model in sales_df["Mobile_Model"].unique():

    model_data = sales_df[sales_df["Mobile_Model"] == model]

    monthly_sales = (
        model_data
        .groupby("Month")
        .size()
    )

    if len(monthly_sales) >= 2:

        avg_sales = monthly_sales.tail(3).mean()

        predicted_units = round(avg_sales)

        suggested_stock = round(predicted_units * 1.2)

        if predicted_units >= 3:
            action = "Increase Stock"
        elif predicted_units == 2:
            action = "Maintain Stock"
        else:
            action = "Low Demand"

        prediction_results.append([
            model,
            predicted_units,
            suggested_stock,
            action
        ])

prediction_df = pd.DataFrame(
    prediction_results,
    columns=[
        "Mobile Model",
        "Expected Sales Next Month",
        "Recommended Stock",
        "Suggestion"
    ]
)

st.dataframe(prediction_df, use_container_width=True)

