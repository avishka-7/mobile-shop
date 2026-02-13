import streamlit as st

st.set_page_config(
    page_title="Mobile Shop System",
    layout="wide"
)

# ---------- BACKGROUND IMAGE ----------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1510552776732-01acc0a61d1e");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.overlay {
    background-color: rgba(0, 0, 0, 0.75);
    padding: 80px;
    border-radius: 20px;
    text-align: center;
    color: white;
}

.title {
    font-size: 48px;
    font-weight: bold;
}

.subtitle {
    font-size: 20px;
    margin-top: 10px;
    opacity: 0.9;
}

.feature-box {
    background-color: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.feature-box:hover {
    background-color: rgba(255,255,255,0.15);
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.markdown("""
<div class="overlay">
    <div class="title"> Mobile Retail Management System</div>
    <div class="subtitle">
        Smart Sales Analytics & Inventory Intelligence for Modern Retailers
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- FEATURES ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>➕ Add Sales</h3>
        <p>Record daily mobile transactions easily.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>📦 Manage Inventory</h3>
        <p>Track stock and avoid shortage risks.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Analytics</h3>
        <p>Understand sales trends and brand performance.</p>
    </div>
    """, unsafe_allow_html=True)
