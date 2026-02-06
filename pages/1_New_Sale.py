import streamlit as st
import csv

st.title("➕ New Sale Entry")

name = st.text_input("Customer Name")
mobile = st.text_input("Mobile Number")

model = st.selectbox(
    "Mobile Model",
    ["Samsung Galaxy S23", "iPhone 14", "Redmi Note 13", "Realme 12 Pro", "OnePlus Nord CE"]
)

price_map = {
    "Samsung Galaxy S series": 75000,
    "IPhone ": 85000,
    "Redmi Note ": 18000,
    "Realme Pro": 25000,
    "OnePlus Nord CE": 30000
}

price = price_map[model]
st.text(f"Price: ₹{price}")

payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "EMI"])

if st.button("Save Sale"):
    if name and mobile.isdigit() and len(mobile) == 10:
        with open("mobile_sales.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, mobile, model, price, payment])
        st.success("Sale saved successfully!")
    else:
        st.error("Enter valid details")
