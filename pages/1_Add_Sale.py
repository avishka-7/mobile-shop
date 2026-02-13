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
        ["Cash", "UPI", "Card","EMI"]
    )

    submitted = st.form_submit_button("Save Sale")

# ---------- SAVE LOGIC ----------
# ---------- SAVE LOGIC ----------
if submitted:

    if customer_name.strip() == "" or mobile_model.strip() == "":
        st.error("Please fill all required fields.")

    else:
        try:
            # Load inventory
            inventory_df = pd.read_csv("inventory.csv")

            # Check if model exists
            if mobile_model not in inventory_df["Mobile_Model"].values:
                st.error("This model is not available in inventory.")

            else:
                # Get current stock
                current_stock = inventory_df.loc[
                    inventory_df["Mobile_Model"] == mobile_model,
                    "Current_Stock"
                ].values[0]

                if current_stock <= 0:
                    st.error("Stock not available for this model.")

                else:
                    # Reduce stock by 1
                    inventory_df.loc[
                        inventory_df["Mobile_Model"] == mobile_model,
                        "Current_Stock"
                    ] = current_stock - 1

                    # Save updated inventory
                    inventory_df.to_csv("inventory.csv", index=False)

                    # Prepare new sale record
                    new_data = pd.DataFrame([{
                        "Date": sale_date.strftime("%d-%m-%Y"),
                        "Customer_Name": customer_name,
                        "Mobile_Model": mobile_model,
                        "Price": price,
                        "Payment_Mode": payment_mode
                    }])

                    # Save sale
                    try:
                        new_data.to_csv("mobile_sales.csv", mode="a", header=False, index=False)
                    except FileNotFoundError:
                        new_data.to_csv("mobile_sales.csv", index=False)

                    st.success("Sale recorded & stock updated successfully!")

                    st.write("Last 5 Records")
                    st.dataframe(pd.read_csv("mobile_sales.csv").tail())

        except FileNotFoundError:
            st.error("Inventory file not found. Please create inventory first.")

