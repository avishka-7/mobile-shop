import streamlit as st
import pandas as pd
import os

st.title("📋 Sales Records")

if os.path.exists("mobile_sales.csv"):
    df = pd.read_csv(
        "mobile_sales.csv",
        names=["Customer Name", "Mobile", "Model", "Price", "Payment"]
    )
    st.dataframe(df)
else:
    st.warning("No sales data available")
