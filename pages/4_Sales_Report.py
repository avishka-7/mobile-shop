import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("📊 Sales Report & Analysis")

if os.path.exists("mobile_sales.csv"):
    df = pd.read_csv(
        "mobile_sales.csv",
        names=["Customer Name", "Mobile", "Model", "Price", "Payment"]
    )

    st.subheader("Sales Summary")
    st.metric("Total Sales", len(df))
    st.metric("Total Revenue", f"₹{df['Price'].sum()}")
    st.metric("Most Sold Model", df["Model"].mode()[0])

    st.subheader("Sales Count per Model")
    fig1, ax1 = plt.subplots()
    df["Model"].value_counts().plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    st.subheader("Revenue Distribution")
    fig2, ax2 = plt.subplots()
    df.groupby("Model")["Price"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    st.pyplot(fig2)
else:
    st.warning("No data available")
