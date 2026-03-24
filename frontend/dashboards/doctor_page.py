import streamlit as st
import requests
from api import get_lab_tests
from datetime import datetime
from api import update_appointment_status
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def doctor_dashboard():

    st.header("🩺 Doctor Dashboard")

    doctor_id = st.session_state["user_id"]

    # Load Appointments
    res = requests.get(
        f"{BASE_URL}/appointments/doctor/{doctor_id}",
        params={"user_id": doctor_id}
    )

    st.markdown('<div class="section-title">📅 My Appointments</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("🔍 Search Patient ID")

    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Accepted", "Rejected"]
        )

    if res.status_code == 200:

        appointments = res.json()

        now = datetime.now()

        appointments = [
            a for a in appointments
            if datetime.fromisoformat(a["appointment_date"]) >= now
        ]

        appointments = sorted(
            appointments,
            key=lambda a: datetime.fromisoformat(a["appointment_date"])
        )
        # Apply filters
        if search:
            appointments = [a for a in appointments if search in str(a["patient_id"])]

        for a in appointments:
            if "status" not in a:
                a["status"] = "Pending"

        if filter_status != "All":
            appointments = [
                a for a in appointments
                if a["status"].lower() == filter_status.lower()
            ]

        if appointments:
            st.markdown('<div class="section-title">🩺 Doctor Dashboard</div>', unsafe_allow_html=True)

            for a in appointments:

                 # highlight first (nearest) appointment
                if a == appointments[0]:
                    st.markdown("### ⏰ Next Appointment")

                status = a.get("status", "Pending")

                # Format date nicely
                dt = datetime.fromisoformat(a["appointment_date"])
                formatted_date = dt.strftime("%d %B %Y | %I:%M %p")

                # Card UI
                status_class = f"status-{status.lower()}"

                st.markdown(f"""
                <div class="card">
                    <h4>🩺 Appointment #{a['id']}</h4>
                    <p><b>👤 Patient ID:</b> {a['patient_id']}</p>
                    <p><b>📅 Date:</b> {formatted_date}</p>
                    <p><b>📝 Reason:</b> {a['reason'].capitalize()}</p>
                    <p class="{status_class}">Status: {status}</p>
                </div>
                """, unsafe_allow_html=True)

                # Buttons only for pending
                if status == "Pending":

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("✅ Accept", key=f"accept_{a['id']}"):
                            res = update_appointment_status(a["id"], "Accepted")
                            st.success("Appointment Accepted")
                            st.rerun()

                    with col2:
                        if st.button("❌ Reject", key=f"reject_{a['id']}"):
                            res = update_appointment_status(a["id"], "Rejected")
                            st.warning("Appointment Rejected")
                            st.rerun()
                    
        else:
                st.info("No appointments scheduled")

    else:
        st.error(res.text)

    # -------------------------------
    # LAB REPORTS SECTION
    # -------------------------------

    st.subheader("🧪 Lab Reports")

    res = get_lab_tests()

    if res.status_code == 200:

        tests = res.json()

        if tests:

            for t in tests:

                # Status color
                status_color = "orange" if not t["result"] else "lightgreen"
                result_text = t["result"] if t["result"] else "Pending"

                st.markdown(f"""
                <div class="card">
                    <h4>🧪 {t['test_name']}</h4>
                    <p><b>Appointment ID:</b> {t['appointment_id']}</p>
                    <p><b>Patient ID:</b> {t['patient_id']}</p>
                    <p><b>Result:</b> {result_text}</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No lab reports available")

    else:
        st.error("Failed to load lab tests")