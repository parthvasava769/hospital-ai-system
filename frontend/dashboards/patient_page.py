import streamlit as st
from api import create_appointment, get_doctors, get_my_appointments
from datetime import datetime
from datetime import time as dt_time
from api import get_lab_tests
from streamlit_autorefresh import st_autorefresh
import requests
from ui_config import ICON_MAP, render_header


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

    render_header("AI Assistant", "ai")

    with st.container():

        command = st.text_input(
            "Describe your issue",
            placeholder="e.g., Book appointment with Dr Smith tomorrow at 10"
        )

        if st.button("Run AI Assistant"):
            if not command:
                st.warning("Please enter a command")
            else:
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

        appointments = [
            a for a in appointments
            if 2020 <= datetime.fromisoformat(a["appointment_date"]).year <= 2030
        ]

        render_header("My Appointments", "appointments")
        show_appointments = st.toggle("Show My Appointments", value=True)

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
                if prev is not None and prev != status:
                    if status == "Accepted":
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
                                <b><i class="bi bi-{ICON_MAP['appointments']}"></i> Appointment #{aid}</b><br>
                                <b>Date:</b> {format_datetime(a['appointment_date'])}<br>
                                <b>Reason:</b> {a['reason']}<br>
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

        if date.year > 2030 or date.year < 2020:
            st.error("Invalid date selected")
            st.stop()

        # Generate time slots (every 15 minutes)
        time_slots = [
        dt_time(hour, minute)
        for hour in range(9, 19)   # 9 AM to 6:45 PM
        for minute in (0, 15, 30, 45)
        ]

        # Convert to readable format
        time_labels = [t.strftime("%I:%M %p") for t in time_slots]

        selected_time_label = st.selectbox(
            "Select Appointment Time",
            time_labels
        )

        # Convert back to time object
        time = datetime.strptime(selected_time_label, "%I:%M %p").time()

        if st.button("Book Appointment", key="book_btn"):

            appointment_datetime = datetime.combine(date, time).isoformat()

            data = {
                "patient_id": st.session_state["user_id"],
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

    
    render_header("My Bills", "billing")

    with st.container():

        res = requests.get(f"{BASE_URL}/billing/patient/{patient_id}")

        if res.status_code == 200:

            bills = res.json()

        # 🛑 SAFETY CHECK
        if isinstance(bills, list):

            for bill in bills:

             if not isinstance(bill, dict):
                continue  # skip bad data silently

            st.markdown(f"""
            <div class="card" style="margin-bottom:15px;">
                <b>💳 Amount:</b> ₹{bill.get('amount', 'N/A')}<br>
                <b>Status:</b> {bill.get('status', 'N/A')}
            </div>
            """, unsafe_allow_html=True)

            if bill.get("status") == "pending":
                if st.button(f"Pay ₹{bill['amount']}", key=f"pay_{bill['id']}"):
                    st.session_state["pay_bill_id"] = bill["id"]
        else:
          st.error("Bills data is not a list")      
        

    # 💳 PAYMENT POPUP UI (PASTE HERE)
    if st.session_state.get("pay_bill_id"):

        render_header("Payment Gateway", "billing")

        col1, col2 = st.columns(2)

        with col1:
            card = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            expiry = st.text_input("Expiry", placeholder="MM/YY")

        with col2:
            cvv = st.text_input("CVV", type="password")
            name = st.text_input("Cardholder Name")

        colA, colB = st.columns(2)

        with colA:
            if st.button("Confirm Payment"):
                with st.spinner("Processing payment..."):
                    import time
                    time.sleep(1.5)

                requests.put(f"{BASE_URL}/pay-bill/{st.session_state['pay_bill_id']}")

                st.success("✅ Payment Successful!")

                st.session_state["pay_bill_id"] = None
                st.rerun()

        with colB:
            if st.button("Cancel"):
                st.session_state["pay_bill_id"] = None
                st.rerun()


    render_header("My Lab Reports", "lab")

    res = get_lab_tests()

    if res.status_code == 200:
        tests = res.json()

        for t in tests:
            if t["patient_id"] == st.session_state["user_id"]:

                status = t.get("result", "Unknown")

                st.markdown(f"""
                <div class="card">
                    <b><i class="bi bi-{ICON_MAP['lab']}"></i> {t['test_name']}</b><br>
                    <b>Result:</b> 
                    <span style="color:{'limegreen' if status.lower()=='positive' else '#f87171'}">
                        {status}
                    </span>
                </div>
                """, unsafe_allow_html=True)