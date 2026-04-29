import streamlit as st
import requests
from api import get_appointments, BASE_URL
from datetime import datetime
from ui_config import ICON_MAP, render_header


def lab_dashboard():

    render_header("Lab Dashboard", "lab")

    # ---------------------------
    # FETCH APPOINTMENTS
    # ---------------------------
    appointments = get_appointments().json()

    def format_date(dt):
        try:
            return datetime.fromisoformat(dt).strftime("%d %b %Y • %I:%M %p")
        except:
            return dt

    appointment_map = {
        f"Appt #{a['id']} • P{a['patient_id']} • {format_date(a['appointment_date'])}": a['id']
        for a in appointments
    }

    # ---------------------------
    # CREATE TEST SECTION
    # ---------------------------
    st.markdown(f"""
        <div style="
            font-size:20px;
            font-weight:600;
            margin-top:20px;
            margin-bottom:10px;
            color:#cbd5f5;
        ">
            <i class="bi bi-{ICON_MAP['add']}"></i> Create Lab Test
        </div>
        """, unsafe_allow_html=True)
    
    
    with st.container():

        selected = st.selectbox("Select Appointment", appointment_map.keys())
        appointment_id = appointment_map[selected]

        # Derive patient_id from the selected appointment
        selected_appointment = next(
            a for a in appointments if a["id"] == appointment_id
        )
        patient_id = selected_appointment["patient_id"]

        

        st.info(f"Patient ID: {patient_id}")

        test_name = st.text_input("Test Name")
        result = st.text_input("Result")


    if st.button("Create Test"):

        # region agent log
        try:
            import json, time  # lightweight, standard library
            with open("debug-c3864d.log", "a", encoding="utf-8") as _f:
                _f.write(
                    json.dumps(
                        {
                            "sessionId": "c3864d",
                            "runId": "pre-fix",
                            "hypothesisId": "A",
                            "location": "frontend/dashboards/lab_page.py:38",
                            "message": "Create Test pressed",
                            "data": {
                                "appointment_id": appointment_id,
                                "patient_id": patient_id,
                            },
                            "timestamp": int(time.time() * 1000),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # endregion

        data = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "test_name": test_name,
            "result": result,
        }

        res = requests.post(
            f"{BASE_URL}/lab-tests",
            json=data
        )

        if res.status_code == 200:
            st.success("✅ Test created successfully")
        else:
            st.error(res.text)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------
    # UPDATE TEST SECTION
    # ---------------------------
    st.markdown('<div class="section-title">✏️ Update Test Result</div>', unsafe_allow_html=True)
    with st.container():

        col1, col2 = st.columns(2)

        with col1:
            test_id = int(st.number_input("Test ID", step=1))

        with col2:
            updated_result = st.text_input("New Result")

    if st.button("Update Result"):
        res = requests.put(
            f"{BASE_URL}/lab-tests/{test_id}",
            json={"result": updated_result}
        )

        if res.status_code == 200:
            st.success("✅ Result updated successfully")
        else:
            st.error(res.text)

    st.markdown('</div>', unsafe_allow_html=True)