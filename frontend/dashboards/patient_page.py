import streamlit as st
from api import create_appointment, get_doctors, get_my_appointments
from datetime import datetime
from api import get_lab_tests
from streamlit_autorefresh import st_autorefresh
import requests

def format_datetime(dt_string):
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return dt_string

BASE_URL = "http://127.0.0.1:8000"



def patient_dashboard():

    if "last_status_map" not in st.session_state:
        st.session_state["last_status_map"] = {}

    st.markdown('<div class="section-title">🤖 AI Assistant</div>', unsafe_allow_html=True)

    with st.container():

        command = st.text_input(
            "Describe your issue",
            placeholder="e.g., Book appointment with Dr Smith tomorrow at 10"
        )

        if st.button("Run AI Assistant"):
            res = requests.post(
                f"{BASE_URL}/ai-assistance/command",
                json={"command": command},
                params={"user_id": st.session_state["user_id"]}
            )

            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error(res.text)

    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

    st.subheader("Book Appointment")

    patient_id = st.session_state["user_id"]
    
    res = get_my_appointments(patient_id)

    if res.status_code == 200:
        appointments = res.json()

        st.markdown('<div class="section-title">📅 My Appointments</div>', unsafe_allow_html=True)
        show_appointments = st.toggle("📅 Show My Appointments", value=True)

        if show_appointments:

            col1, col2, col3 = st.columns(3)

            col1.metric("Total", len(appointments))
            col2.metric("Pending", sum(1 for a in appointments if a.get("status") == "Pending"))
            col3.metric("Accepted", sum(1 for a in appointments if a.get("status") == "Accepted"))

            for a in appointments:
                aid = a["id"]
                status = a.get("status", "Pending")
                status_lower = status.lower() 

                prev = st.session_state["last_status_map"].get(aid)
                print("DEBUG →", aid, prev, status)

                # 🔔 Show notification only if status changed
                if prev and prev != status:
                    if prev is not None and prev != status:
                        st.toast(f"✅ Appointment #{aid} Accepted")
                    elif status == "Rejected":
                        st.toast(f"❌ Appointment #{aid} Rejected")

                # update stored state
                st.session_state["last_status_map"][aid] = status

                # 🎯 CLEAN CARD
                col1, col2 = st.columns([3,1])

                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <b>🩺 Appointment #{aid}</b><br>
                        📅 {format_datetime(a['appointment_date'])}<br>
                        📝 {a['reason']}<br>
                        <span class="status-{status_lower}">● {status}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(" ")  # spacing
    res = get_doctors()

    if res.status_code == 200:

        doctors = res.json()

        doctor_names = {
            f"{d['name']} (ID: {d['id']})": d["id"]
            for d in doctors
        }

        selected = st.selectbox(
            "Select Doctor",
            doctor_names.keys(),
            key="doctor_select"
        )

        doctor_id = doctor_names[selected]

        reason = st.text_input("Reason")

        date = st.date_input("Select Appointment Date")

        time = st.time_input("Select Appointment Time")

        if st.button("Book Appointment"):

            appointment_datetime = datetime.combine(date, time).isoformat()

            data = {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": appointment_datetime,
                "reason": reason
            }

            res = create_appointment(
                data,
                st.session_state["user_id"]
            )

            if res.status_code == 200:
                st.success("Appointment booked")
            else:
                st.error(res.text)

    else:
        st.error("Failed to load doctors")
    
    st.subheader("My Lab Reports")

    res = get_lab_tests()

    if res.status_code == 200:
        tests = res.json()

        for t in tests:
            if t["patient_id"] == st.session_state["user_id"]:
                st.write(f"Test: {t['test_name']}")
                st.write(f"Result: {t['result']}")
                st.divider()