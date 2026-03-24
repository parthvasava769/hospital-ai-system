import streamlit as st

from auth.login_page import login_page
from auth.register_page import register_page

from dashboards.patient_page import patient_dashboard
from dashboards.doctor_page import doctor_dashboard
from dashboards.lab_page import lab_dashboard
from dashboards.ai_page import ai_dashboard

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)


# ---------------------------
# THEME INIT
# ---------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
# ---------------------------
# GLOBAL STYLING
# ---------------------------

st.markdown("""
    <style>

    /* 🌙 DARK BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 20% 20%, #1e3a8a, transparent 40%),
                    radial-gradient(circle at 80% 30%, #9333ea, transparent 40%),
                    radial-gradient(circle at 50% 80%, #0f172a, #020617);
    }

    /* 🏥 Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #0f172a);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Header clean */
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Keep toggle */
    [data-testid="stToolbar"] > div:not(:first-child) {
        display: none;
    }

    /* Toggle button */
    [data-testid="collapsedControl"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }

    /* Cards */
    .card {
        background: rgba(17, 24, 39, 0.9);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }

    /* Inputs */
    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.05) !important;
        color: white;
        border-radius: 10px;
        padding-right: 40px;
    }

    /* Password icon */
    button[title="Show password"],
    button[title="Hide password"] {
        right: 10px !important;
    }

    /* Remove helper */
    [data-testid="stTextInput"] small {
        display: none !important;
    }

    /* Buttons */
    [data-testid="stButton"] button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-radius: 10px;
        height: 45px;
    }

    /* Titles */
    h1 a, h2 a, h3 a {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)

if st.session_state.get("theme") == "light":
    st.markdown("""
    <style>

   /*LIGHT BACKGROUND*/

    /* Root layers */
    html, body {
        background: #f8fafc !important;
    }

    .stApp {
        background: #f8fafc !important;
    }

    /* Main container */
    section.main {
        background: transparent !important;
    }

    /* App container */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 10% 20%, #c7d2fe, transparent 40%),
            radial-gradient(circle at 90% 30%, #e9d5ff, transparent 40%),
            #f8fafc !important;
    }

    /* 🔥 REMOVE ALL DARK INNER WRAPPERS */
    [data-testid="stAppViewContainer"] > div,
    [data-testid="stAppViewContainer"] > div > div,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="element-container"],
    div[data-testid="column"],
    div[data-testid="column"] > div {
        background: transparent !important;
    }

    /* 🔥 VERY IMPORTANT (portal fix) */
    div[role="listbox"],
    div[data-baseweb="popover"] {
        background: white !important;
    }

    /* 🔥 SCROLLABLE DARK AREAS */
    div[style*="overflow"] {
        background: transparent !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.85) !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: #0f172a !important;
    }

    /* Cards */
    .card {
        background: rgba(255,255,255,0.9) !important;
        color: #0f172a !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* Inputs FIX */
    [data-testid="stTextInput"] input {
        background: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
    }

    /* Dropdown FIX */
    [data-baseweb="select"],
    [data-baseweb="select"] div {
        background: white !important;
        color: black !important;
    }

    /* Date input */
    [data-testid="stDateInput"] input {
        color: black !important;
        background: white !important;
    }

    /* Time input */
    [data-testid="stTimeInput"] input {
        background: white !important;
        color: black !important;
    }

    /* Button */
    [data-testid="stButton"] button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
    }

    /* TEXT SYSTEM */
    h1, h2, h3 { color: #020617 !important; }
    p, label, span, div { color: #1e293b !important; }

    input::placeholder {
        color: #64748b !important;
    }

    /* 🔥 FIX DROPDOWN POPUP (CRITICAL FIX) */
    div[data-baseweb="popover"] {
        background: white !important;
        color: black !important;
    }

    /* dropdown list items */
    div[data-baseweb="menu"] {
        background: white !important;
    }

    /* each option */
    div[role="option"] {
        color: black !important;
    }

    /* selected option */
    div[aria-selected="true"] {
        background: #e0e7ff !important;
        color: black !important;
    }

    /* hover option */
    div[role="option"]:hover {
        background: #f1f5f9 !important;
    }

    /* REMOVE RED BORDER */
    [data-baseweb="select"] {
        border: 1px solid #ddd !important;
        box-shadow: none !important;
    }

    /* NUMBER INPUT FIX */
    [data-testid="stNumberInput"] input {
        background: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align:center;
    font-size:28px;
    font-weight:700;
    margin-bottom:20px;
">
    🏥 Hospital Management System
</div>
""", unsafe_allow_html=True)
# ---------------------------
# SESSION INIT
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------------------------
# NOT LOGGED IN
# ---------------------------
if not st.session_state["logged_in"]:

    st.sidebar.markdown("## 🏥 HMS Panel")
    st.sidebar.divider()

    theme_toggle = st.sidebar.toggle(
        "Light Mode",
        value=(st.session_state.get("theme") == "light")
    )

    if theme_toggle:
        if st.session_state.get("theme") != "light":
            st.session_state["theme"] = "light"
            st.rerun()
    else:
        if st.session_state.get("theme") != "dark":
            st.session_state["theme"] = "dark"
            st.rerun()
    
    menu = st.sidebar.radio(
        "Navigation",
        ["Login", "Register"]
    )

    # 🏥 LANDING PAGE
    if menu == "Home":

        st.markdown("""
        <div style="text-align:center; margin-top:50px;">
            <h1 style="font-size:40px;">🏥 Hospital Management System</h1>
            <p style="font-size:18px; color:gray;">
                Smart Healthcare. Seamless Experience.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="card" style="text-align:center;">
                🤖<br><b>AI Assistant</b><br>
                Book appointments using natural language
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                🩺<br><b>Doctor Dashboard</b><br>
                Manage appointments efficiently
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="card" style="text-align:center;">
                🧪<br><b>Lab System</b><br>
                Track and update reports
            </div>
            """, unsafe_allow_html=True)

    elif menu == "Login":
        login_page()

    elif menu == "Register":
        register_page()
# ---------------------------
# LOGGED IN
# ---------------------------
else:

    role = st.session_state["role"]

    st.sidebar.title("🏥 Hospital System")
    st.sidebar.success(f"Logged in as {role}")

    theme_toggle = st.sidebar.toggle("Light Mode", value=False)
    st.session_state["theme"] = "light" if theme_toggle else "dark"

    # 🔥 NEW PROFESSIONAL NAVIGATION
    if role == "patient":
        page = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "AI Assistant"]
        )

        if page == "Dashboard":
            patient_dashboard()

        elif page == "AI Assistant":
            ai_dashboard()

    elif role == "doctor":
        doctor_dashboard()

    elif role == "lab_staff":
        lab_dashboard()

    # ---------------------------
    # LOGOUT BUTTON
    # ---------------------------
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()