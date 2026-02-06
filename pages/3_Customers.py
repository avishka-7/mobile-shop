import streamlit as st
import pandas as pd
import os

st.title("👤 Customer Records")

if os.path.exists("mobile_sales.csv"):
    df = pd.read_csv(
        "mobile_sales.csv",
        names=["Customer Name", "Mobile", "Model", "Price", "Payment"]
    )
    customers = df[["Customer Name", "Mobile"]].drop_duplicates()
    st.dataframe(customers)
else:
    st.warning("No customer data available")
