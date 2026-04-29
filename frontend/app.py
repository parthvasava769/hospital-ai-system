import streamlit as st
from streamlit.elements.widgets.select_slider import SelectSliderSerde

from auth.login_page import login_page
from auth.register_page import register_page

from dashboards.patient_page import patient_dashboard
from dashboards.doctor_page import doctor_dashboard
from dashboards.lab_page import lab_dashboard
from dashboards.ai_page import ai_dashboard
from dashboards.admin_page import admin_dashboard
from streamlit_option_menu import option_menu
from ui_config import ICON_MAP
from ui_config import render_sidebar_header

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");
    i.bi {
        font-family: "bootstrap-icons" !important;
        font-style: normal;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

    transition: 
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border 0.25s ease;

    border: 1px solid rgba(255,255,255,0.05);
    }

    /* HOVER EFFECT */
    .card:hover {
        transform: translateY(-6px) scale(1.01);

        box-shadow: 
            0 20px 50px rgba(0,0,0,0.8),
            0 0 25px rgba(139,92,246,0.25);

    border: 1px solid rgba(139,92,246,0.3);
    }
    
    /* TRANSITIONS */
    * {
        transition: all 0.2s ease-in-out;
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


st.markdown("""
<div style="
    text-align:center;
    font-size:28px;
    font-weight:700;
    margin-bottom:20px;
">
    <i class="bi bi-hospital"></i> Hospital Management System
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

    st.sidebar.markdown("## <i class='bi bi-hospital'></i> HMS Panel", unsafe_allow_html=True)
    st.sidebar.divider()

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
                <i class="bi bi-robot"></i><br><b>AI Assistant</b><br>
                Book appointments using natural language
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <i class="bi bi-person-badge"></i><br><b>Doctor Dashboard</b><br>
                Manage appointments efficiently
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <i class="bi bi-flask"></i><br><b>Lab System</b><br>
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

    with st.sidebar:
        render_sidebar_header("Hospital System", "hospital", "Management Panel")
        st.success(f"Logged in as {role}")

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

    elif role == "admin":
        admin_dashboard()

    # ---------------------------
    # LOGOUT BUTTON
    # ---------------------------
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()