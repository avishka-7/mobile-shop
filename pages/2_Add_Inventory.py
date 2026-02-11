import streamlit as st
import pandas as pd

st.set_page_config(page_title="Add Inventory", layout="wide")

st.title("📦 Add / Update Inventory")

# ---------- LOAD INVENTORY ----------
try:
    inventory_df = pd.read_csv("inventory.csv")
except FileNotFoundError:
    inventory_df = pd.DataFrame(columns=["Mobile_Model", "Current_Stock"])

# ---------- FORM ----------
with st.form("inventory_form"):

    col1, col2 = st.columns(2)

    with col1:
        mobile_model = st.text_input("Mobile Model")

    with col2:
        stock = st.number_input("Stock Quantity", min_value=0)

    submitted = st.form_submit_button("Save / Update")

# ---------- SAVE LOGIC ----------
if submitted:

    if mobile_model.strip() == "":
        st.error("Please enter a mobile model.")
    else:
        if mobile_model in inventory_df["Mobile_Model"].values:
            # Update stock
            inventory_df.loc[
                inventory_df["Mobile_Model"] == mobile_model,
                "Current_Stock"
            ] = stock
            st.success("Inventory updated successfully!")
        else:
            # Add new model
            new_row = pd.DataFrame([{
                "Mobile_Model": mobile_model,
                "Current_Stock": stock
            }])
            inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
            st.success("New inventory added successfully!")

        inventory_df.to_csv("inventory.csv", index=False)

# ---------- VIEW INVENTORY ----------
st.markdown("---")
st.subheader("📋 Current Inventory")

st.dataframe(inventory_df)
