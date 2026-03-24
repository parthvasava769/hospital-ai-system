import streamlit as st
from api import login_user


def login_page():

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # 🏥 Logo + Title
        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:42px;">🏥</div>
            <div style="font-size:24px; font-weight:600;">Login Portal</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        
        # 👉 Inputs OUTSIDE (important)
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login", use_container_width=True):

            res = login_user({
                "email": email,
                "password": password
            })

            if res.status_code == 200:
                user = res.json()

                st.session_state["logged_in"] = True
                st.session_state["role"] = user["role"]
                st.session_state["user_id"] = user["user_id"]

                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")