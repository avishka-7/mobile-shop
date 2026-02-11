import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Status", layout="wide")

st.title("📦 Stock Status Overview")

# ---------- LOAD DATA ----------
sales_df = pd.read_csv("sales.csv")
inventory_df = pd.read_csv("inventory.csv")

sales_df.columns = sales_df.columns.str.strip()
inventory_df.columns = inventory_df.columns.str.strip()

# Convert date
sales_df["Date"] = pd.to_datetime(
    sales_df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_df = sales_df.dropna(subset=["Date"])

# ---------- SALES PER MODEL ----------
sales_count = sales_df["Mobile_Model"].value_counts().reset_index()
sales_count.columns = ["Mobile_Model", "Units_Sold"]

# ---------- MERGE ----------
merged_df = pd.merge(
    inventory_df,
    sales_count,
    on="Mobile_Model",
    how="left"
)

merged_df["Units_Sold"] = merged_df["Units_Sold"].fillna(0)

# ---------- STOCK DIFFERENCE ----------
merged_df["Stock_Remaining"] = (
    merged_df["Current_Stock"] - merged_df["Units_Sold"]
)

# ---------- STATUS CLASSIFICATION ----------
def classify(row):
    if row["Stock_Remaining"] < 5:
        return "🔴 Low Stock"
    elif row["Stock_Remaining"] <= 15:
        return "🟡 Moderate"
    else:
        return "🟢 Sufficient"

merged_df["Status"] = merged_df.apply(classify, axis=1)

# ---------- DISPLAY ----------
st.subheader("Inventory vs Sales")

st.dataframe(merged_df)

st.markdown("---")

# ---------- SUMMARY ----------
low_stock = merged_df[merged_df["Status"] == "🔴 Low Stock"]

if not low_stock.empty:
    st.error(f"⚠️ {len(low_stock)} models are low in stock. Consider restocking.")
else:
    st.success("All stock levels are Sufficient.")
