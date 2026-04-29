import streamlit as st
import requests
from ui_config import ICON_MAP, render_header

BASE_URL = "http://127.0.0.1:8000"

def admin_dashboard():
    render_header("Admin Dashboard", "settings")

    menu = st.sidebar.selectbox("Manage", ["Users", "Appointments"])

    st.subheader("Add New User")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["patient", "doctor", "lab_staff"])

    if st.button("Create User"):
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
            "role": role
        }

        res = requests.post(f"{BASE_URL}/register", json=data)

        if res.status_code == 200:
            st.success("User created")
            st.rerun()
        else:
            st.error(res.text)

    # ---------------- USERS ----------------
    if menu == "Users":
        st.subheader("Manage Users")

        res = requests.get(f"{BASE_URL}/admin/users")

        if res.status_code == 200:
            users = res.json()

            for user in users:
                st.markdown(f"""
                <div class="card">
                    <i class="bi bi-{ICON_MAP['patients']}"></i> <b>{user['name']}</b><br>
                    {user['email']}<br>
                    Role: {user['role']}
                </div>
                """, unsafe_allow_html=True)

                # ❌ DELETE BUTTON
                if st.button(f"Delete User {user['id']}", key=f"del_{user['id']}"):
                    requests.delete(f"{BASE_URL}/admin/users/{user['id']}")
                    st.success("User deleted")
                    st.rerun()

        else:
            st.error("Failed to load users")

    # ---------------- APPOINTMENTS ----------------
    elif menu == "Appointments":
        st.subheader("All Appointments")

        res = requests.get(f"{BASE_URL}/admin/appointments")

        if res.status_code == 200:
            appointments = res.json()

            for a in appointments:
                st.markdown(f"""
                <div class="card">
                    <i class="bi bi-{ICON_MAP['appointments']}"></i> Appointment #{a['id']}<br>
                    {a['appointment_date']}<br>
                    Patient ID: {a['patient_id']}<br>
                    Doctor ID: {a['doctor_id']}<br>
                    Status: {a['status']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Failed to load appointments")