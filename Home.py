import streamlit as st

st.set_page_config(
    page_title="Mobile Retail System",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 40px;
}

.hero h1 {
    font-size: 48px;
    color: white;
}

.hero p {
    font-size: 20px;
    color: #d1d5db;
}

/* Feature Cards */
.card {
    background-color: #1f2937;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    transition: 0.3s;
}

.card:hover {
    background-color: #2d3748;
    transform: translateY(-5px);
}

.card h3 {
    color: white;
}

.card p {
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <h1> Mobile Retail Management System</h1>
    <p>Smart Sales Analytics & Inventory Intelligence for Modern Retailers</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURE SECTION ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>➕ Add Sales</h3>
        <p>Record daily mobile transactions quickly and accurately.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📦 Manage Inventory</h3>
        <p>Track stock levels and avoid shortage or overstock risks.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>📊 Analytics</h3>
        <p>Understand sales trends, brand performance & revenue insights.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")



Use the sidebar to navigate through the system.
"""
)


