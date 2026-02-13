import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Mobile Shop System",
    layout="wide"
)

# ---------- SIDEBAR TITLE ----------
st.markdown("""
<style>
[data-testid="stSidebar"]::before {
    content: "📱 Mobile Shop System";
    display: block;
    font-size: 22px;
    font-weight: bold;
    padding: 20px 20px 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- MAIN PAGE STYLING ----------
st.markdown("""
<style>
.main-container {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 60px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.big-title {
    font-size: 46px;
    font-weight: bold;
}

.subtitle {
    font-size: 20px;
    opacity: 0.9;
    margin-top: 10px;
}

.feature-box {
    background-color: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.feature-box:hover {
    background-color: rgba(255,255,255,0.1);
    transform: scale(1.03);
}

.footer-note {
    text-align: center;
    opacity: 0.6;
    font-size: 14px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.markdown("""
<div class="main-container">
    <div class="big-title">📱 Mobile Retail Management System</div>
    <div class="subtitle">
        AI-Driven Sales Analytics & Smart Inventory Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- FEATURES SECTION ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>➕ Add Sales</h3>
        <p>Record daily transactions quickly and efficiently.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3> Manage Inventory</h3>
        <p>Track stock levels and avoid shortages or overstock.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3> View Analytics</h3>
        <p>Analyze performance with interactive dashboards.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer-note">
    Built with Streamlit • Data-Driven Decision Support for Retailers
</div>
""", unsafe_allow_html=True)

