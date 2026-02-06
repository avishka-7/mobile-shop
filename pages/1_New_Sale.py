import streamlit as st
import csv

st.title("➕ New Sale Entry")

name = st.text_input("Customer Name")
mobile = st.text_input("Mobile Number")

# ✅ Allow ANY mobile model
model = st.text_input("Mobile Model (Any brand / any model)")

# ✅ Allow manual price entry
price = st.number_input(
    "Price (₹)",
    min_value=0,
    step=500
)

payment = st.selectbox(
    "Payment Mode",
    ["Cash", "UPI", "Card", "EMI"]
)

if st.button("Save Sale"):
    if not name:
        st.error("Customer name is required")
    elif not mobile.isdigit() or len(mobile) != 10:
        st.error("Enter a valid 10-digit mobile number")
    elif not model:
        st.error("Enter mobile model")
    elif price <= 0:
        st.error("Enter valid price")
    else:
        with open("mobile_sales.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, mobile, model, price, payment])

        st.success("✅ Sale recorded successfully")
