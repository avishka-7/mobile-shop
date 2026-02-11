import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Mobile Retail System", layout="wide")

# ---------- CUSTOM COLOR THEME ----------
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f9;
        }
        .title-style {
            font-size: 40px;
            font-weight: 700;
            color: #2c3e50;
        }
        .welcome-box {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
            font-size: 17px;
            color: #444;
        }
        .highlight {
            color: #1f77b4;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<div class='title-style'>📱 Mobile Retail Management System</div>", unsafe_allow_html=True)

st.markdown(" ")

# ---------- WELCOME BOX ----------
st.markdown("""
<div class='welcome-box'>
Welcome to the <span class='highlight'>AI-driven Mobile Retail Analytics System</span>.<br><br>

Use the sidebar to:
<ul>
<li>Add Sales</li>
<li>Add Inventory</li>
<li>View Analytics</li>
<li>Predict Demand</li>
</ul>
</div>
""", unsafe_allow_html=True)
