import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Add Sale", layout="wide")

st.title("➕ Add New Sale")

# ---------- FORM ----------
with st.form("sale_form"):

    col1, col2 = st.columns(2)

    with col1:
        sale_date = st.date_input("Sale Date", date.today())
        customer_name = st.text_input("Customer Name")

    with col2:
        mobile_model = st.text_input("Mobile Model")
        price = st.number_input("Price (₹)", min_value=0)

    payment_mode = st.selectbox(
        "Payment Mode",
        ["Cash", "UPI", "Card"]
    )

    submitted = st.form_submit_button("Save Sale")

# ---------- SAVE LOGIC ----------
if submitted:

    if customer_name.strip() == "" or mobile_model.strip() == "":
        st.error("Please fill all required fields.")
    else:
        new_data = pd.DataFrame([{
            "Date": sale_date.strftime("%d-%m-%Y"),
            "Customer_Name": customer_name,
            "Mobile_Model": mobile_model,
            "Price": price,
            "Payment_Mode": payment_mode
        }])

        try:
            new_data.to_csv("sales.csv", mode="a", header=False, index=False)
        except FileNotFoundError:
            new_data.to_csv("sales.csv", index=False)

        st.success("Sale recorded successfully!")
