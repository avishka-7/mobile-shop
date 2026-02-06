import streamlit as st

st.set_page_config(
    page_title="Mobile Shop Management System",
    layout="centered"
)

st.title("📱 Mobile Shop Management System")

st.markdown("""
### Welcome!
Use the sidebar to navigate through the application.

**Features:**
- New Sale Entry
- View Sales Records
- Customer Records
- Sales Summary & Analysis
""")

st.info("Select a page from the sidebar")
